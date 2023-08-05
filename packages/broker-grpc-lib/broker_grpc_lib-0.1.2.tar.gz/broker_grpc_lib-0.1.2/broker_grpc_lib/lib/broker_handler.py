from abc import ABC, abstractmethod

from typing import Any, Type, TypeVar, Union
from pydantic import BaseModel
from .grpc_client import GRPCClient

import asyncio
import signal

T = TypeVar("T", bound=BaseModel)
RequestType = TypeVar("RequestType")


class BrokerHandler(ABC):

    def __init__(
            self,
            host: str,
            login: str,
            password: str,
            port: int,
            grpc_stub: GRPCClient,
            grpc_request_cls: RequestType,
            grpc_method_name: str,
            schema: Union[Any, Type[T], Type[BaseModel]]
    ):
        self._host = host
        self._login = login
        self._password = password
        self._port = port
        self._grpc_stub = grpc_stub
        self._grpc_request_cls = grpc_request_cls
        self._grpc_method_name = grpc_method_name
        self._schema = schema

    @abstractmethod
    async def start(self):
        raise NotImplementedError

    @abstractmethod
    async def _handle_message(self, message):
        raise NotImplementedError

    async def write_message(self, message_body: bytes):
        raise NotImplementedError

    @abstractmethod
    async def stop(self):
        raise NotImplementedError

    async def wait_for_termination(self):
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.stop()))

        await asyncio.Future()
