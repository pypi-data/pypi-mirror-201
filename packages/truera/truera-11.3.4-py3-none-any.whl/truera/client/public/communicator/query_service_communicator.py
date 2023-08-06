from abc import ABC
from abc import abstractmethod

from truera.authn.usercontext import RequestContext
from truera.protobuf.queryservice import query_service_pb2 as qs_pb


class AbstractQueryServiceCommunicator(ABC):

    @abstractmethod
    def echo(self, request: qs_pb.EchoRequest) -> qs_pb.EchoResponse:
        pass

    @abstractmethod
    def query(
        self, request: qs_pb.QueryRequest, request_context: RequestContext
    ) -> qs_pb.QueryResponse:
        pass
