# pylint: disable=no-name-in-module,no-member
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb
from truera.protobuf.public.util import split_mode_pb2

# pylint: enable=no-name-in-module

DEFAULT_SAMPLE_STRATEGY = ds_messages_pb.SAMPLE_RANDOM
DEFAULT_APPROX_MAX_ROWS = 1_000_000
DEFAULT_SPLIT_TYPE = "all"
DEFAULT_SPLIT_MODE = split_mode_pb2.SplitMode.SPLIT_MODE_DATA_REQUIRED

PROD_DATA_SPLIT_TYPE = "prod"
SPECIAL_COLUMN_NAMES = {
    "__truera_id__",
}
