from __future__ import annotations

import datetime
import logging
import os
import sys
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

from cachetools import cached
from cachetools import LRUCache
import numpy as np
import pandas as pd

from truera.analytics.loader.schema_loader import CsvSchemaConfiguration
from truera.analytics.utils.cache_utils import get_cache_size_limit_from_config
from truera.protobuf.public.common.schema_pb2 import \
    ColumnDetails  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.data_split_pb2 import \
    DataSplit  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    StaticDataTypeEnum  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.split_mode_pb2 import \
    SplitMode  # pylint: disable=no-name-in-module
from truera.utils.config_util import get_config_value
from truera.utils.datetime_util.datetime_parse_util import \
    get_datetime_from_proto_string
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraNotFoundError

# TODO: intelligently pick default by amount of mem?
_DEFAULT_SPLIT_DATA_CACHE_SIZE_LIMIT_BYTES = 1e9
SPLIT_DATA_CACHE_SIZE_LIMIT_BYTES = get_cache_size_limit_from_config(
    "split_cache_size_limit_bytes", _DEFAULT_SPLIT_DATA_CACHE_SIZE_LIMIT_BYTES
)

STATIC_DATA_TYPE_CONVERSION = {
    StaticDataTypeEnum.STRING:
        str,
    StaticDataTypeEnum.BOOL:
        bool,
    StaticDataTypeEnum.INT8:
        np.int8,
    StaticDataTypeEnum.INT16:
        np.int16,
    StaticDataTypeEnum.INT32:
        np.int32,
    StaticDataTypeEnum.INT64:
        np.int64,
    StaticDataTypeEnum.INTPTR:
        np.intp,
    StaticDataTypeEnum.UINT8:
        np.uint8,
    StaticDataTypeEnum.UINT16:
        np.uint16,
    StaticDataTypeEnum.UINT32:
        np.uint32,
    StaticDataTypeEnum.UINT64:
        np.uint64,
    StaticDataTypeEnum.UINTPTR:
        np.uintp,
    StaticDataTypeEnum.FLOAT32:
        np.float32,
    StaticDataTypeEnum.FLOAT64:
        np.float64,
    StaticDataTypeEnum.DATETIME:
        np.datetime64,
    StaticDataTypeEnum.DATETIME64:
        np.datetime64,
    #StaticDataTypeEnum.COMPLEXFLOAT32: None,
    StaticDataTypeEnum.COMPLEXFLOAT64:
        np.complex64,
    StaticDataTypeEnum.COERCEDBINARY:
        np.int32,
}


class DataTypesHelper:

    @staticmethod
    def get_dtypes_map(columns: List[ColumnDetails]) -> Dict[str, type]:
        # TODO(AB#3334): This doesn't handle integer_options_type and string_options_type.
        return {
            col.name:
            STATIC_DATA_TYPE_CONVERSION[col.data_type.static_data_type]
            for col in columns
            if col.data_type.static_data_type != StaticDataTypeEnum.INVALID
        }


def _check_df_column_type_matches(df: pd.DataFrame):
    logger = logging.getLogger(__name__)
    for column in df.columns:
        column_data = df[column]
        cell_type_series = column_data.apply(type)
        logger.info(cell_type_series)
        if cell_type_series.nunique() == 1:
            continue

        # More than 1 value detected.
        column_dtype = column_data.dtype
        first_value_type = cell_type_series.iloc[0]
        first_nonmatching = cell_type_series.ne(first_value_type).idxmax()
        raise ValueError(
            (
                "Found column '{}' (dtype {}) with mismatched data. First value is '{}' (with type {}), but found nonmatching value '{}' (with type {}) at row {}"
            ).format(
                column, column_data.iloc[0], column_dtype, first_value_type,
                column_data.iloc[first_nonmatching],
                cell_type_series.iloc[first_nonmatching], first_nonmatching
            )
        )
    pass


class DataReader(object):

    def __init__(
        self,
        server_config: dict,
        missing_values: Optional[Sequence[str]] = None
    ):
        if missing_values is None:
            missing_values = []
        self.server_config = server_config
        self.missing_values = missing_values
        self.logger = logging.getLogger(__name__)

    def read_csv(
        self,
        path: str,
        dtypes: Optional[Mapping[str, type]] = None,
        *,
        header_none: bool = False,
        column_names: Optional[List[str]] = None
    ) -> pd.DataFrame:
        data_read_row_limit = self.get_max_rows_to_read()
        kwargs = {}
        if header_none:
            kwargs["header"] = None
        if column_names:
            kwargs["names"] = column_names

        dtypes_no_dates = {}
        date_columns = []
        if dtypes is not None:
            for key in dtypes:
                if dtypes[key] == np.datetime64:
                    date_columns.append(key)
                else:
                    dtypes_no_dates[key] = dtypes[key]

        df = pd.read_csv(
            path,
            keep_default_na=False,
            na_values=self.missing_values,
            nrows=data_read_row_limit,
            dtype=dtypes_no_dates,
            parse_dates=date_columns,
            **kwargs
        )

        if get_config_value(
            self.server_config, "user_data_reader", "enable_fill_na", False
        ):
            str_fill_na = get_config_value(
                self.server_config, "user_data_reader", "fill_na_string_col", ""
            )
            numeric_fill_na = get_config_value(
                self.server_config, "user_data_reader", "fill_na_numeric_col",
                float("NaN")
            )

            columns = list(df.columns)
            dtypes = df.dtypes
            for column in columns:
                is_str_column = dtypes[columns.index(column)] == "object"
                if is_str_column:
                    df[column].fillna(str_fill_na, inplace=True)
                else:
                    df[column].fillna(numeric_fill_na, inplace=True)

        check_type_matches = get_config_value(
            self.server_config, "user_data_reader", "check_column_type_matches",
            False
        )
        if check_type_matches:
            _check_df_column_type_matches(df)

        return df

    def get_max_rows_to_read(self):
        return get_config_value(
            self.server_config, "user_data_reader", "data_read_row_limit", 50000
        )


class Dataset(object):
    """Represents the dataset used to generate a model.
    
    """

    def __init__(
        self,
        dataset_id: str,
        splits: Sequence[DataSplit],
        schema_info: CsvSchemaConfiguration,
        *,
        data_reader: DataReader = DataReader({}),
        project_id: str = 'default',
    ):
        self.logger = logging.getLogger('ailens.Dataset')
        self.dataset_id = dataset_id
        self.project_id = project_id
        self.logger.debug("Creating dataset %s", self.dataset_id)
        self.data_reader = data_reader
        self.schema_info = schema_info
        self._splits: Mapping[str, SplitInfo] = {
            sp.id: SplitInfo(sp, data_reader, schema_info=schema_info)
            for sp in splits
        }
        self._base_split_id: str = ""

    def set_base_split_id(self, base_split_id: str):
        self._base_split_id = base_split_id

    def get_base_split_id(self) -> Optional[str]:
        return self._base_split_id

    def get_split(self, split_id: str) -> Optional['SplitInfo']:
        split_id = split_id or self.get_base_split_id()

        if not split_id:
            return None
        if split_id not in self._splits:
            raise TruEraNotFoundError(
                f"No such split {split_id} in {list(self._splits.keys())}"
            )

        return self._splits[split_id]

    def get_splits(self) -> Sequence['SplitInfo']:
        """gets a list of splits"""

        return self._splits.values()

    def remove_split(self, id):
        if id not in self._splits:
            self.logger.warning(
                "Trying to delete non-existent split %s from dataset %s", id,
                self.dataset_id
            )
            return
        del self._splits[id]

    def add_split(self, split: DataSplit):
        if split.id in self._splits:
            raise ValueError(
                'Tried to add duplicate split {} to dataset {}'.format(
                    split.id, self.dataset_id
                )
            )
        self._splits[split.id
                    ] = SplitInfo(split, self.data_reader, self.schema_info)


class SplitInfo:
    CACHE_SIZE_IN_BYTES = SPLIT_DATA_CACHE_SIZE_LIMIT_BYTES
    """
    devnote: pre, post, extra, and label data are read and cached using an LRUCache.
    LRUCache implementations are NOT instance-specific; that is, a singular cache is shared across
    all instances of SplitInfo. In addition, deletions of a given SplitInfo object will NOT garbage
    collect the respective cache entries in the shared cache. 

    we avoid stale cache results by including the SplitInfo object creation time in the cache key itself,
    and assume items from the cache are only evicted when the cache reaches its max size.
    """

    def __init__(
        self, proto: DataSplit, data_reader: DataReader,
        schema_info: CsvSchemaConfiguration
    ):
        # TODO: Is this logger visible?
        self.logger = logging.getLogger(__name__)
        self.proto = proto
        self._set_last_updated_on()
        self.data_reader = data_reader
        self.feature_list = schema_info
        self._preprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.pre_schema
        )
        self._postprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.post_schema
        )
        self._extraprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.extra_schema
        )
        self._labelprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.label_schema
        )

        # system data may include system ID cols, timestamp cols, etc. that should be ignored for analytics
        self._label_column_name: Optional[str] = None

        self.split_id = proto.id
        self.split_name = proto.name
        self.split_type = proto.split_type
        self.split_mode = proto.split_mode

        self._loaded = False
        self._is_valid: Optional[bool] = None
        self._validation_exception = None
        self._num_rows_preprocessed: Optional[int] = None
        self._preprocessed_feature_names: Optional[Sequence[str]] = None
        self._postprocessed_feature_names: Optional[Sequence[str]] = None

        self._creation_time = datetime.datetime.now()

    def _set_last_updated_on(self):
        self.updated_on = get_datetime_from_proto_string(self.proto.updated_on)

    @property
    def num_inputs(self) -> int:
        if self.split_mode == SplitMode.SPLIT_MODE_PREDS_REQUIRED:
            # NB: We are assuming here that full labels are provided and that they are always aligned to predictions.
            return len(self.label_data)
        if self._num_rows_preprocessed is None:
            self._read_preprocessed_data()
        return self._num_rows_preprocessed

    @property
    def feature_names(self) -> Iterable[str]:
        if not self._preprocessed_feature_names:
            self._preprocessed_feature_names = list(
                self.preprocessed_data.columns
            )
        return self._preprocessed_feature_names

    @property
    def processed_feature_names(self) -> Iterable[str]:
        if not self._postprocessed_feature_names:
            self._postprocessed_feature_names = list(
                self.processed_data.columns
            )
        return self._postprocessed_feature_names

    @property
    def pre_transform_locator(self) -> str:
        return self.proto.preprocessed_locator

    @property
    def post_transform_locator(self) -> str:
        return self.proto.processed_locator

    @property
    def label_locator(self) -> str:
        return self.proto.label_locator

    @property
    def unique_id_column_name(self) -> str:
        return self.proto.unique_id_column_name

    @property
    def timestamp_column_name(self) -> str:
        return self.proto.timestamp_column_name

    @property
    def label_column_name(self) -> str:
        if not self._label_column_name:
            self._read_label_data()
        return self._label_column_name

    @property
    def system_column_names(self) -> Sequence[str]:
        return [
            col
            for col in [self.unique_id_column_name, self.timestamp_column_name]
            if col
        ]

    def _read_preprocessed_data(self) -> Optional[pd.DataFrame]:
        if self.proto.preprocessed_locator:
            ret_df = self.data_reader.read_csv(
                self.proto.preprocessed_locator, self._preprocessed_dtypes
            )
            if self.unique_id_column_name:
                ret_df.set_index(self.unique_id_column_name, inplace=True)
            self._num_rows_preprocessed = len(ret_df)
            return ret_df

    def _read_processed_data(self) -> Optional[pd.DataFrame]:
        if self.proto.processed_locator and os.path.exists(
            self.proto.processed_locator
        ):
            ret_df = self.data_reader.read_csv(
                self.proto.processed_locator, self._postprocessed_dtypes
            )
            if self.unique_id_column_name:
                ret_df.set_index(self.unique_id_column_name, inplace=True)
            self.validate_processed_data(ret_df)
            return ret_df

    def _read_label_data(self) -> Optional[pd.DataFrame]:
        if self.proto.label_locator and os.path.exists(
            self.proto.label_locator
        ):
            # This is done temporarily to support label file with and without header
            # for backward compatibility.
            if "__internal_with_headers" in os.path.basename(
                self.proto.label_locator
            ):
                label_df = self.data_reader.read_csv(
                    self.proto.label_locator, self._labelprocessed_dtypes
                )
                unaccounted_cols = [
                    col for col in label_df.columns
                    if col not in self.system_column_names
                ]
                if len(unaccounted_cols) > 1:
                    raise TruEraInternalError(
                        f"Label data has unrecognized columns {unaccounted_cols}!"
                    )
                self._label_column_name = unaccounted_cols[0]
                if self.unique_id_column_name:
                    label_df.set_index(self.unique_id_column_name, inplace=True)
                return label_df.reindex(
                    self.processed_or_preprocessed_data_with_system_data.index
                )
            else:
                # assume labels without headers are one-column CSVs fully aligned to pre-data, and assigns a header to them
                self._label_column_name = "ground_truth"
                return self.data_reader.read_csv(
                    self.proto.label_locator,
                    self._labelprocessed_dtypes,
                    header_none=True,
                    column_names=[self._label_column_name]
                )

    def _read_extra_data(self) -> Optional[pd.DataFrame]:
        if self.proto.extra_data_locator and os.path.exists(
            self.proto.extra_data_locator
        ):
            ret_df = self.data_reader.read_csv(
                self.proto.extra_data_locator, self._extraprocessed_dtypes
            )
            if self.unique_id_column_name:
                ret_df.set_index(self.unique_id_column_name, inplace=True)
            self.validate_extra_data(ret_df)
            return ret_df

    @property
    @cached(
        cache=LRUCache(maxsize=CACHE_SIZE_IN_BYTES, getsizeof=sys.getsizeof),
        key=lambda x: (x.proto.preprocessed_locator, x._creation_time)
    )
    def preprocessed_data_with_system_data(self) -> Optional[pd.DataFrame]:
        return self._read_preprocessed_data()

    @property
    def preprocessed_data(self) -> pd.DataFrame:
        if self.timestamp_column_name:
            return self.preprocessed_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.preprocessed_data_with_system_data

    @property
    @cached(
        cache=LRUCache(maxsize=CACHE_SIZE_IN_BYTES, getsizeof=sys.getsizeof),
        key=lambda x: (x.proto.processed_locator, x._creation_time)
    )
    def processed_data_with_system_data(self) -> Optional[pd.DataFrame]:
        return self._read_processed_data()

    @property
    def processed_data(self) -> pd.DataFrame:
        if self.timestamp_column_name and self.processed_data_with_system_data is not None:
            return self.processed_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.processed_data_with_system_data

    @property
    @cached(
        cache=LRUCache(maxsize=CACHE_SIZE_IN_BYTES, getsizeof=sys.getsizeof),
        key=lambda x: (x.proto.label_locator, x._creation_time)
    )
    def label_data_with_system_data(self) -> pd.DataFrame:
        return self._read_label_data()

    @property
    def label_data(self) -> pd.DataFrame:
        label_df = self.label_data_with_system_data
        if self.timestamp_column_name and label_df is not None:
            return label_df.drop(self.timestamp_column_name, axis="columns")
        return label_df

    @property
    @cached(
        cache=LRUCache(maxsize=CACHE_SIZE_IN_BYTES, getsizeof=sys.getsizeof),
        key=lambda x: (x.proto.extra_data_locator, x._creation_time)
    )
    def extra_data_with_system_data(self) -> Optional[pd.DataFrame]:
        return self._read_extra_data()

    @property
    def extra_data(self) -> pd.DataFrame:
        if self.timestamp_column_name and self.extra_data_with_system_data is not None:
            return self.extra_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.extra_data_with_system_data

    @property
    def has_labels(self) -> bool:
        return self.label_data is not None

    @property
    def processed_or_preprocessed_data(self) -> pd.DataFrame:
        return self.processed_data if self.processed_data is not None else self.preprocessed_data

    @property
    def processed_or_preprocessed_data_with_system_data(self) -> pd.DataFrame:
        return self.processed_data_with_system_data if self.processed_data_with_system_data is not None else self.preprocessed_data_with_system_data

    def validate_processed_data(
        self, processed_data_with_system_data: Optional[pd.DataFrame]
    ):
        if processed_data_with_system_data is not None and self.preprocessed_data_with_system_data is not None and len(
            processed_data_with_system_data
        ) != len(self.preprocessed_data_with_system_data):
            raise TruEraInternalError(
                f"Data mismatch in split {self.split_id}! Preprocessed data has {len(self.preprocessed_data_with_system_data)} rows. Postprocessed data has {len(processed_data_with_system_data)} rows."
            )

    def validate_extra_data(
        self, extra_data_with_system_data: Optional[pd.DataFrame]
    ):
        if extra_data_with_system_data is not None and self.preprocessed_data_with_system_data is not None and len(
            extra_data_with_system_data
        ) != len(self.preprocessed_data_with_system_data):
            raise TruEraInternalError(
                f"Data mismatch in split {self.split_id}! Preprocessed data has {len(self.preprocessed_data_with_system_data)} rows. Extra data has {len(extra_data_with_system_data)} rows."
            )
