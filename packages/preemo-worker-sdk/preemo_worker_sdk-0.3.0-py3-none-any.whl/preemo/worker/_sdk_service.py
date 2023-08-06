from typing import Callable, Optional

import grpc
from google.protobuf.struct_pb2 import NULL_VALUE

from preemo.gen.endpoints.execute_function_pb2 import (
    ExecuteFunctionRequest,
    ExecuteFunctionResponse,
)
from preemo.gen.endpoints.terminate_pb2 import TerminateRequest, TerminateResponse
from preemo.gen.models.value_pb2 import Value
from preemo.gen.services.sdk_pb2_grpc import SDKServiceServicer
from preemo.worker._artifact_manager import ArtifactId, IArtifactManager
from preemo.worker._function_registry import FunctionRegistry
from preemo.worker._types import assert_never


class SDKService(SDKServiceServicer):
    @staticmethod
    def _validate_execute_function_request(request: ExecuteFunctionRequest) -> None:
        if not request.HasField("function_to_execute"):
            raise Exception(
                "expected ExecuteFunctionRequest to have function_to_execute"
            )

        if not request.function_to_execute.HasField("name"):
            raise Exception("expected RegisteredFunction to have name")

        if not request.HasField("parameter"):
            raise Exception("expected ExecuteFunctionRequest to have parameter")

    def __init__(
        self,
        *,
        artifact_manager: IArtifactManager,
        function_registry: FunctionRegistry,
        terminate_server: Callable[[], None],
    ) -> None:
        self._artifact_manager = artifact_manager
        self._function_registry = function_registry
        self._terminate_server = terminate_server

    def _retrieve_value(self, value: Value) -> Optional[bytes]:
        kind = value.WhichOneof("kind")
        if kind is None:
            raise Exception("expected value to have kind")

        if kind == "null_value":
            return None

        if kind == "artifact_id":
            return self._artifact_manager.get_artifact(
                ArtifactId(value=value.artifact_id)
            )

        assert_never(kind)

    def ExecuteFunction(
        self, request: ExecuteFunctionRequest, context: grpc.ServicerContext
    ) -> ExecuteFunctionResponse:
        SDKService._validate_execute_function_request(request)

        if request.function_to_execute.HasField("namespace"):
            namespace = request.function_to_execute.namespace
        else:
            namespace = None

        func = self._function_registry.get_required_function(
            name=request.function_to_execute.name, namespace=namespace
        )

        parameter_value = self._retrieve_value(request.parameter)
        if parameter_value is None:
            result = func()
        else:
            result = func(parameter_value)

        if result is None:
            result_value = Value(null_value=NULL_VALUE)
        else:
            # TODO(adrian@preemo.io, 04/04/2023): validate that result is bytes?
            result_artifact_id = self._artifact_manager.create_artifact(result)
            result_value = Value(artifact_id=result_artifact_id.value)

        return ExecuteFunctionResponse(result=result_value)

    def Terminate(
        self, request: TerminateRequest, context: grpc.ServicerContext
    ) -> TerminateResponse:
        self._terminate_server()
        return TerminateResponse()
