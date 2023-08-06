import aio_pika
from aio_pika.pool import Pool
from aio_pika import Channel, Message
from aio_pika.abc import AbstractRobustConnection

from .broker_handler import BaseModel, BrokerHandler, T, RequestType
from .grpc_client import GRPCClient
from ..exc.no_queue_exception import NoReadQueueException, NoWriteQueueException

import asyncio
import signal
import grpc

from pydantic.error_wrappers import ValidationError
from typing import Any, Type, Union

import logging
logging.basicConfig(level=logging.INFO)


class RabbitMQHandler(BrokerHandler):

    def __init__(
            self,
            host: str,
            login: str,
            password: str,
            port: int,
            grpc_stub: GRPCClient,
            grpc_method_name: str,
            grpc_request_cls: RequestType,
            schema: Union[Any, Type[T], Type[BaseModel]],
            max_connections: int,
            max_channels: int,
            write_queue_name: Union[str, None] = None,
            read_queue_name: Union[str, None] = None,
            callback_queue_name: Union[str, None] = None
    ):
        super().__init__(
            host=host,
            login=login,
            password=password,
            port=port,
            grpc_stub=grpc_stub,
            grpc_method_name=grpc_method_name,
            grpc_request_cls=grpc_request_cls,
            schema=schema,
        )
        self._read_queue_name = read_queue_name
        self._write_queue_name = write_queue_name
        self._callback_queue_name = callback_queue_name
        self._max_connections = max_connections
        self._max_channels = max_channels
        self._channel_pool: Union[None, Pool] = None
        self._connection_pool: Union[None, Pool] = None
        self._loop = asyncio.get_running_loop()

        assert self._read_queue_name or self._write_queue_name, "No queues were passed"

    async def __init_pools(self) -> bool:
        self._connection_pool = Pool(self.__get_connection, max_size=self._max_connections, loop=self._loop)
        self._channel_pool = Pool(self.__get_channel, max_size=self._max_channels, loop=self._loop)

        return True

    async def __init_queues(self) -> bool:
        for _ in range(self._max_channels):
            async with self._channel_pool.acquire() as channel:
                if self._read_queue_name:
                    await channel.declare_queue(self._read_queue_name)
                if self._write_queue_name:
                    await channel.declare_queue(self._write_queue_name)
                if self._callback_queue_name:
                    await channel.declare_queue(self._callback_queue_name)

        return True

    async def prepare_handler(self):
        pools = await self.__init_pools()
        queues = await self.__init_queues()

        return pools and queues

    async def __get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host=self._host,
            login=self._login,
            password=self._password,
            port=self._port
        )

    async def __get_channel(self) -> Channel:
        async with self._connection_pool.acquire() as connection:
            return await connection.channel()

    async def start(self):
        if not self._read_queue_name:
            raise NoReadQueueException("No read queue")

        async with self._channel_pool.acquire() as channel:
            queue = await channel.get_queue(self._read_queue_name)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await self._handle_message(message)

    async def _handle_message(self, message: Message):
        # TODO: Callback queue?
        try:
            message_body = self._schema.parse_raw(message.body)
            request = self._grpc_request_cls(**message_body.dict(exclude_unset=True))
            _ = await self._grpc_stub.execute(method_name=self._grpc_method_name, request=request)
        except ValidationError as e:
            logging.error(f"Invalid message: {str(e)}")
        except grpc.RpcError as e:
            logging.error(f"gRPC Error: {str(e)}")

    async def write_message(self, message_body: bytes):
        if not self._write_queue_name:
            raise NoWriteQueueException("No write queue")

        async with self._channel_pool.acquire() as channel:
            # TODO: Либо передавать название очереди как параметр и отправлять через `routing_key`,
            #  а не в конкретную очередь
            queue = await channel.get_queue(self._write_queue_name)
            message = Message(body=message_body)
            await queue.publish(message)

    async def stop(self):
        if not self._connection_pool.is_closed:
            await self._connection_pool.close()
        if not self._channel_pool.is_closed:
            await self._channel_pool.close()
        logging.info("RabbitMQ connection_pool, channel_pool and grpc_channel were closed")

    async def wait_for_termination(self):
        self._loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))
        self._loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.stop()))

        await asyncio.Future()
