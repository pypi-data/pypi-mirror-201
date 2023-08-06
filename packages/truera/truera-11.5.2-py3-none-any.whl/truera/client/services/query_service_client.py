from __future__ import annotations

from collections import defaultdict
import logging
from typing import Optional, Sequence, Tuple

import pandas as pd

from truera.authn.usercontext import RequestContext
from truera.client.private.communicator.query_service_grpc_communicator import \
    GrpcQueryServiceCommunicator
from truera.client.public.auth_details import AuthDetails
import truera.protobuf.public.common_pb2 as common_pb
from truera.protobuf.public.qoi_pb2 import \
    QuantityOfInterest  # pylint: disable=no-name-in-module
from truera.protobuf.queryservice import query_service_pb2 as qs_pb
from truera.utils.data_constants import NORMALIZED_EVENT_TIMESTAMP_COLUMN_NAME
from truera.utils.data_constants import NORMALIZED_ID_COLUMN_NAME
from truera.utils.data_constants import \
    NORMALIZED_INGESTION_TIMESTAMP_COLUMN_NAME
from truera.utils.data_constants import NORMALIZED_TIMESTAMP_COLUMN_NAME
from truera.utils.datetime_util.datetime_parse_util import \
    parse_timestamp_from_dataframe
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraNotFoundError

value_extractors = {
    "BYTE":
        lambda x: x.byte_value,
    "INT16":
        lambda x: x.short_value,
    "INT32":
        lambda x: x.int_value,
    "INT64":
        lambda x: x.long_value,
    "FLOAT":
        lambda x: x.float_value,
    "DOUBLE":
        lambda x: x.double_value,
    "STRING":
        lambda x: x.string_value,
    "BOOLEAN":
        lambda x: x.bool_value,
    "TIMESTAMP":
        lambda x: pd.Timestamp(x.timestamp_value.seconds, unit='s').
        to_datetime64()
}

dtype_conversion_dict = {
    "BYTE": "int8",
    "INT16": "int16",
    "INT32": "int32",
    "INT64": "int64",
    "FLOAT": "float32",
    "DOUBLE": "float64",
    "STRING": "str",
    "BOOLEAN": "bool",
    "TIMESTAMP": "datetime64"
}

TRUERA_SPLIT_ID_COL = "__truera_split_id__"


class QueryServiceClient(object):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails = None,
        logger=None
    ):
        self.communicator = GrpcQueryServiceCommunicator(
            connection_string, auth_details, logger
        )
        self.logger = logger or logging.getLogger(__name__)
        self.value_extractors_dict = value_extractors
        self.dtypes_dict = dtype_conversion_dict

    def echo(self, request_id: str, message: str) -> qs_pb.EchoResponse:
        self.logger.info(
            f"QueryServiceClient::echo request_id={request_id}, message={message}"
        )
        request = qs_pb.EchoRequest(request_id=request_id, message=message)
        response = self.communicator.echo(request)
        return response

    def getPreprocessedData(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, include_system_data: bool, request_id: str,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        return self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_PRE",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getProcessedOrPreprocessedData(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, include_system_data: bool, request_id: str,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        try:
            return self._read_static_data(
                project_id=project_id,
                data_collection_id=data_collection_id,
                query_spec=query_spec,
                expected_data_kind="DATA_KIND_POST",
                include_system_data=include_system_data,
                request_id=request_id,
                request_context=request_context
            )
        except TruEraNotFoundError:
            return self._read_static_data(
                project_id=project_id,
                data_collection_id=data_collection_id,
                query_spec=query_spec,
                expected_data_kind="DATA_KIND_PRE",
                include_system_data=include_system_data,
                request_id=request_id,
                request_context=request_context
            )

    def getLabels(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, include_system_data: bool, request_id: str,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        return self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_LABEL",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getExtraData(
        self,
        project_id: str,
        data_collection_id: str,
        query_spec: qs_pb.QuerySpec,
        include_system_data: bool,
        request_id: str,
        request_context: RequestContext,
    ) -> pd.DataFrame:
        return self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_EXTRA",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getModelPredictions(
        self, project_id: str, model_id: str, query_spec: qs_pb.QuerySpec,
        quantity_of_interest: QuantityOfInterest,
        classification_threshold: float, include_system_data: bool,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        request = qs_pb.QueryRequest(
            id=request_context.get_request_id(),
            project_id=project_id,
            prediction_request=qs_pb.PredictionRequest(
                model_id=model_id,
                qoi=quantity_of_interest,
                query_spec=query_spec,
                classification_threshold=classification_threshold
            )
        )
        dataframe = self._pb_stream_to_dataframe(
            self.communicator.query(request, request_context)
        )
        if NORMALIZED_EVENT_TIMESTAMP_COLUMN_NAME in dataframe.columns:
            dataframe.drop(
                columns=[NORMALIZED_EVENT_TIMESTAMP_COLUMN_NAME], inplace=True
            )
            self.logger.info(
                f"Dropping {NORMALIZED_EVENT_TIMESTAMP_COLUMN_NAME}."
            )
        if NORMALIZED_INGESTION_TIMESTAMP_COLUMN_NAME in dataframe.columns:
            dataframe.drop(
                columns=[NORMALIZED_INGESTION_TIMESTAMP_COLUMN_NAME],
                inplace=True
            )
            self.logger.info(
                f"Dropping {NORMALIZED_INGESTION_TIMESTAMP_COLUMN_NAME}."
            )

        # standardize prediction col name for downstream use
        prediction_col_name = None
        for col in dataframe.columns:
            if col != NORMALIZED_TIMESTAMP_COLUMN_NAME and col != NORMALIZED_ID_COLUMN_NAME:
                prediction_col_name = col
        assert prediction_col_name
        return parse_timestamp_from_dataframe(
            dataframe,
            NORMALIZED_TIMESTAMP_COLUMN_NAME,
            include_timestamp_col=include_system_data
        ).set_index(NORMALIZED_ID_COLUMN_NAME)

    def getModelInfluences(
        self,
        project_id: str,
        request_context: RequestContext,
        query_spec: qs_pb.QuerySpec,
        options: common_pb.FeatureInfluenceOptions,
        model_id: Optional[str] = None,
        include_system_data: bool = False,
    ) -> Optional[pd.DataFrame]:
        request = qs_pb.QueryRequest(
            id=request_context.get_request_id(),
            project_id=project_id,
            feature_influence_request=qs_pb.FeatureInfluenceRequest(
                model_id=model_id, query_spec=query_spec, options=options
            )
        )
        response_stream = self.communicator.query(request, request_context)
        dataframe = self._pb_stream_to_dataframe(response_stream)

        dataframe = self._resolve_split_metadata(
            dataframe=dataframe,
            include_system_data=include_system_data,
            cols_to_drop=[]
        )
        return dataframe

    def getFilterData(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        request = qs_pb.QueryRequest(
            id=request_context.get_request_id(),
            project_id=project_id,
            filter_data_request=qs_pb.FilterDataRequest(
                data_collection_id=data_collection_id, query_spec=query_spec
            )
        )
        response_stream = self.communicator.query(request, request_context)
        dataframe = self._pb_stream_to_dataframe(response_stream)

        dataframe = self._resolve_split_metadata(
            dataframe=dataframe, include_system_data=False, cols_to_drop=[]
        )
        return dataframe

    def _read_static_data(
        self,
        *,
        project_id: str,
        data_collection_id: str,
        query_spec: qs_pb.QuerySpec,
        expected_data_kind: str,
        include_system_data: bool,
        request_id: str,
        request_context: RequestContext,
    ) -> Optional[pd.DataFrame]:
        request = qs_pb.QueryRequest(
            id=request_id,
            project_id=project_id,
            raw_data_request=qs_pb.RawDataRequest(
                data_kind=expected_data_kind,
                data_collection_id=data_collection_id,
                query_spec=query_spec
            )
        )
        response_stream = self.communicator.query(request, request_context)
        dataframe = self._pb_stream_to_dataframe(response_stream)

        dataframe = self._resolve_split_metadata(
            dataframe=dataframe,
            include_system_data=include_system_data,
            cols_to_drop=[TRUERA_SPLIT_ID_COL]
        )
        return dataframe

    def _pb_stream_to_dataframe(
        self, response_stream: qs_pb.QueryResponse
    ) -> pd.DataFrame:
        first_element = True
        dataframes = []
        extractors = None
        dtypes = None
        table_metadata = None

        for stream_element in response_stream:
            table = stream_element.row_major_value_table
            # only the first element contains the table's metadata
            if first_element:
                first_element = False
                extractors, dtypes, table_metadata = self._process_metadata(
                    table, stream_element.request_id
                )
            # create a dataframe from single pb message/stream element
            df_data = [
                self._extract_row_values(table_metadata, row, extractors)
                for row in table.rows
            ]
            dataframes.append(pd.DataFrame(df_data))

        if len(dataframes) == 0:
            raise TruEraNotFoundError(
                "Could not find any rows in the table corresponding to the requested data kind!"
            )
        return pd.concat(
            dataframes, ignore_index=True, copy=False
        ).astype(dtypes).rename(
            columns={tm.index: tm.name for tm in table_metadata}
        )

    def _process_metadata(
        self, table: qs_pb.QueryResponse.row_major_value_table, request_id: str
    ) -> Tuple[dict, dict, Sequence[qs_pb.ColumnMetadata]]:
        if len(table.metadata) == 0:
            raise TruEraInternalError(
                "table metadata is not available. request_id={}.".
                format(request_id)
            )
        # python formatter is a gift that keeps on giving
        return self._value_extractors_for_response(
            table
        ), self._dtypes_for_response(table), table.metadata

    @staticmethod
    def _extract_row_values(table_metadata, row, extractors) -> dict:
        row_dict = defaultdict()
        for column_meta in table_metadata:
            cell = row.columns[column_meta.index]
            value_extractor = extractors.get(column_meta.index)
            value = value_extractor(cell)
            row_dict[column_meta.index] = value
        return row_dict

    # use qs_pb.ValueType and self.value_extractors_dict to assign a value extractor to each column based on response metadata
    def _value_extractors_for_response(
        self, table: qs_pb.QueryResponse.row_major_value_table
    ) -> dict:
        return {
            column_meta.index: self.value_extractors_dict.get(
                qs_pb.ValueType.Name(column_meta.type)
            ) for column_meta in table.metadata
        }

    # use qs_pb.ValueType and self.dtypes_dict to get dtypes for the dataframe based on response metadata
    def _dtypes_for_response(
        self, table: qs_pb.QueryResponse.row_major_value_table
    ) -> dict:
        return {
            column_meta.index:
            self.dtypes_dict.get(qs_pb.ValueType.Name(column_meta.type))
            for column_meta in table.metadata
        }

    def _resolve_split_metadata(
        self, dataframe: pd.DataFrame, include_system_data: bool,
        cols_to_drop: Sequence[str]
    ) -> pd.DataFrame:
        cols_to_drop.append(NORMALIZED_EVENT_TIMESTAMP_COLUMN_NAME)
        cols_to_drop.append(NORMALIZED_INGESTION_TIMESTAMP_COLUMN_NAME)

        if include_system_data:
            # get datetime from integer epoch, but cast to string for AIQ purposes
            dataframe[NORMALIZED_TIMESTAMP_COLUMN_NAME] = pd.to_datetime(
                dataframe[NORMALIZED_TIMESTAMP_COLUMN_NAME], unit="s"
            ).astype(str)
        else:
            cols_to_drop.append(NORMALIZED_TIMESTAMP_COLUMN_NAME)
        df_columns = list(dataframe.columns)
        cols_to_drop = [c for c in cols_to_drop if c in df_columns]
        dataframe.drop(cols_to_drop, axis="columns", inplace=True)
        dataframe.set_index(NORMALIZED_ID_COLUMN_NAME, inplace=True)
        return dataframe
