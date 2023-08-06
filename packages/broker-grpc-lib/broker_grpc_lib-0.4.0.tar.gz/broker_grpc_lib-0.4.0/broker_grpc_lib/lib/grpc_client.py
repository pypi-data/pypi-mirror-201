import grpc
import signal
import asyncio
from typing import Any


class GRPCClient:

    def __init__(self, stub_cls: Any, grpc_host: str, grpc_port: int):
        self.channel = grpc.aio.insecure_channel(f"{grpc_host}:{grpc_port}")
        self.grpc_stub = stub_cls(self.channel)

    async def execute(self, method_name: str, request: Any) -> Any:
        method = getattr(self.grpc_stub, method_name)
        return await method(request)

    async def cleanup(self):
        await self.channel.close()

    async def wait_for_termination(self):
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.cleanup()))
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.cleanup()))

        await asyncio.Future()
