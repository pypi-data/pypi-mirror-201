from __future__ import annotations

import functools
import json
from typing import Optional, Tuple, TYPE_CHECKING

from google.protobuf.json_format import MessageToDict

import truera.protobuf.public.aiq.intelligence_service_pb2 as i_s_proto
from truera.utils.filter_utils import FilterProcessor

if TYPE_CHECKING:
    import truera.aiq.intelligence_server_impl as impl
    from truera.authn.usercontext import RequestContext

MODEL_METRICS_CACHE_SIZE = 2e7  # performance, fairness and stability have their own caches


def cache_non_pending_op(cache, key):

    def decorator(func):

        def wrapper(*args, **kwargs):
            k = key(*args, **kwargs)
            try:
                return cache[k]
            except KeyError:
                pass  # key not found
            v = func(*args, **kwargs)
            try:
                if hasattr(v, "is_operations"):
                    if not v.is_operations:
                        cache[k] = v
                elif hasattr(v, "pending_operations"):
                    if not v.pending_operations.waiting_on_operation_ids:
                        cache[k] = v
            except ValueError:
                pass  # value too large
            return v

        wrapper.cache = cache
        wrapper.cache_key = key
        wrapper.cache_clear = cache.clear

        return functools.update_wrapper(wrapper, func)

    return decorator


def serialize_proto(proto_msg) -> str:
    return json.dumps(
        MessageToDict(
            proto_msg,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        ),
        sort_keys=True,
        default=str
    )


def resolve_split_id_in_input_spec(
    input_spec: i_s_proto.ModelInputSpec, iss: impl.IntelligenceServiceServicer,
    project_id: str, model_id: str, request_context: RequestContext
) -> i_s_proto.ModelInputSpec:
    split_id = input_spec.split_id or iss.artifact_metadata_client.get_default_base_split_id_for_model(
        request_context, project_id, model_id
    )
    input_spec_with_resolved_split_id = i_s_proto.ModelInputSpec()
    input_spec_with_resolved_split_id.CopyFrom(input_spec)
    input_spec_with_resolved_split_id.split_id = split_id
    return input_spec_with_resolved_split_id
