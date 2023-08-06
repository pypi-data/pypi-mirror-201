import concurrent.futures
import random

import grpc

from preemo.gen.services.sdk_pb2_grpc import add_SDKServiceServicer_to_server
from preemo.worker._artifact_manager import IArtifactManager
from preemo.worker._function_registry import FunctionRegistry
from preemo.worker._sdk_service import SDKService


class SDKServer:
    @staticmethod
    def _generate_random_port() -> int:
        return random.randrange(60_000, 61_000)

    @staticmethod
    def _bind_server_to_random_port(*, server: grpc.Server, host: str) -> int:
        attempt_count = 0
        while True:
            port = SDKServer._generate_random_port()
            try:
                # TODO(adrian@preemo.io, 03/27/2023): investigate whether it makes sense to use add_secure_port instead
                server.add_insecure_port(f"{host}:{port}")
            except RuntimeError as e:
                if len(e.args) < 1:
                    raise e

                message = e.args[0]
                if "Failed to bind to address" not in message:
                    raise e

                print(f"failed to bind to port {port}, retrying with a different port")
            else:
                return port

            attempt_count += 1
            if attempt_count >= 20:
                raise Exception(f"failed to connect {attempt_count} times")

    def __init__(
        self,
        *,
        artifact_manager: IArtifactManager,
        function_registry: FunctionRegistry,
        sdk_server_host: str,
    ) -> None:
        server = grpc.server(
            concurrent.futures.ThreadPoolExecutor(max_workers=1),
            # This option prevents multiple servers from reusing the same port (see https://groups.google.com/g/grpc-io/c/RB69llv2tC4/m/7E__iL3LAwAJ)
            options=(("grpc.so_reuseport", 0),),
        )

        def close() -> None:
            server.stop(grace=10)  # seconds

        add_SDKServiceServicer_to_server(
            SDKService(
                artifact_manager=artifact_manager,
                function_registry=function_registry,
                terminate_server=close,
            ),
            server,
        )
        port = SDKServer._bind_server_to_random_port(
            server=server, host=sdk_server_host
        )

        server.start()
        print(f"sdk server has started on port {port}")

        self._server = server
        self._port = port

    def get_port(self) -> int:
        return self._port

    def wait_until_close(self) -> None:
        self._server.wait_for_termination()
