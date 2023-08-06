from typing import Callable, List, Optional

from google.protobuf.struct_pb2 import NULL_VALUE

from preemo.gen.endpoints.batch_execute_function_pb2 import BatchExecuteFunctionRequest
from preemo.gen.endpoints.check_function_pb2 import CheckFunctionRequest
from preemo.gen.endpoints.register_function_pb2 import RegisterFunctionRequest
from preemo.gen.models.registered_function_pb2 import RegisteredFunction
from preemo.gen.models.value_pb2 import Value
from preemo.worker._artifact_manager import ArtifactId, IArtifactManager
from preemo.worker._function_registry import FunctionRegistry
from preemo.worker._messaging_client import IMessagingClient
from preemo.worker._types import assert_never


class Result:
    # TODO(adrian@preemo.io, 04/20/2023): need to sort out how this class
    # can be used when error handling, status checking, etc
    # Perhaps futures should be used instead
    def __init__(
        self, *, artifact_id: ArtifactId, artifact_manager: IArtifactManager
    ) -> None:
        self._artifact_id = artifact_id
        self._artifact_manager = artifact_manager

    def get(self) -> bytes:
        return self._artifact_manager.get_artifact(self._artifact_id)


class Function:
    def __init__(
        self,
        *,
        artifact_manager: IArtifactManager,
        messaging_client: IMessagingClient,
        name: str,
        namespace: Optional[str],
    ) -> None:
        self._artifact_manager = artifact_manager
        self._messaging_client = messaging_client
        self.name = name
        self.namespace = namespace

        self._ensure_function_is_registered()

    def _ensure_function_is_registered(self) -> None:
        # check_function raises an error if the function is not found
        self._messaging_client.check_function(
            CheckFunctionRequest(
                function_to_check=RegisteredFunction(
                    name=self.name, namespace=self.namespace
                )
            )
        )

    def __call__(self, params: Optional[bytes] = None) -> Optional[Result]:
        if params is None:
            function_parameter = Value(null_value=NULL_VALUE)
        else:
            artifact_id = self._artifact_manager.create_artifact(params)
            function_parameter = Value(artifact_id=artifact_id.value)

        response = self._messaging_client.batch_execute_function(
            BatchExecuteFunctionRequest(
                function_to_execute=RegisteredFunction(
                    name=self.name, namespace=self.namespace
                ),
                parameters_by_index={0: function_parameter},
            )
        )

        function_result = response.results_by_index[0]

        kind = function_result.WhichOneof("kind")
        if kind is None:
            raise Exception("expected kind to be defined")

        if kind == "null_value":
            return None

        if kind == "artifact_id":
            return Result(
                artifact_id=ArtifactId(value=function_result.artifact_id),
                artifact_manager=self._artifact_manager,
            )

        assert_never(kind)


class WorkerClient:
    def __init__(
        self,
        *,
        artifact_manager: IArtifactManager,
        function_registry: FunctionRegistry,
        messaging_client: IMessagingClient,
    ) -> None:
        self._artifact_manager = artifact_manager
        self._messaging_client = messaging_client
        self._function_registry = function_registry

    def get_function(self, name: str, *, namespace: Optional[str] = None) -> Function:
        return Function(
            artifact_manager=self._artifact_manager,
            messaging_client=self._messaging_client,
            name=name,
            namespace=namespace,
        )

    def parallel(
        self,
        function: Function,
        *,
        params: Optional[List[bytes]] = None,
        count: Optional[int] = None,
    ) -> List[Optional[Result]]:
        # TODO(adrian@preemo.io, 03/20/2023): should take an optional config argument includes stuff like max batch size

        if params is None:
            if count is None:
                raise ValueError("either params or count must be specified")

            if count <= 0:
                raise ValueError("count must be positive")

            function_parameters_by_index = {
                i: Value(null_value=NULL_VALUE) for i in range(count)
            }
        else:
            if count is not None:
                raise ValueError("params and count must not both be specified")

            if len(params) == 0:
                return []

            artifact_ids = self._artifact_manager.create_artifacts(params)
            function_parameters_by_index = {
                i: Value(artifact_id=artifact_id.value)
                for i, artifact_id in enumerate(artifact_ids)
            }

        response = self._messaging_client.batch_execute_function(
            BatchExecuteFunctionRequest(
                function_to_execute=RegisteredFunction(
                    name=function.name, namespace=function.namespace
                ),
                parameters_by_index=function_parameters_by_index,
            )
        )

        results: List[Optional[Result]] = []
        for _, function_result in sorted(
            response.results_by_index.items(), key=lambda x: x[0]
        ):
            kind = function_result.WhichOneof("kind")
            if kind is None:
                raise Exception("expected kind to be defined")

            if kind == "null_value":
                results.append(None)
            elif kind == "artifact_id":
                results.append(
                    Result(
                        artifact_id=ArtifactId(value=function_result.artifact_id),
                        artifact_manager=self._artifact_manager,
                    )
                )
            else:
                assert_never(kind)

        return results

    def register(
        self,
        outer_function: Optional[Callable] = None,
        *,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> Callable:
        def decorator(function: Callable) -> Callable:
            if name is None:
                function_name = function.__name__
            else:
                function_name = name

            self._function_registry.register_function(
                function, name=function_name, namespace=namespace
            )

            self._messaging_client.register_function(
                RegisterFunctionRequest(
                    function_to_register=RegisteredFunction(
                        name=function_name, namespace=namespace
                    )
                )
            )

            return function

        if outer_function is None:
            return decorator

        return decorator(outer_function)
