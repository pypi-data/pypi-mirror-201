import pytest
from pytest_mock import MockFixture

from broker_grpc_lib.lib.rabbitmq_handler import RabbitMQHandler
from broker_grpc_lib.lib.broker_handler import BrokerHandler

from tests.helpers.async_iterator import AsyncIterator

import asyncio


class TestRabbitMQHandler:

    @pytest.fixture
    def rabbitmq_host(self):
        return "localhost"

    @pytest.fixture
    def rabbitmq_port(self):
        return 5432

    @pytest.fixture
    def rabbitmq_login(self):
        return "login"

    @pytest.fixture
    def rabbitmq_password(self):
        return "password"

    @pytest.fixture
    def grpc_method_name(self):
        return "method_name"

    @pytest.fixture
    def grpc_stub(self, mocker: MockFixture):
        return mocker.MagicMock(
            execute=mocker.AsyncMock()
        )

    @pytest.fixture
    def grpc_request_cls(self, mocker: MockFixture):
        return mocker.MagicMock()

    @pytest.fixture
    def rabbitmq_max_connections(self):
        return 2

    @pytest.fixture
    def rabbitmq_max_channels(self):
        return 10

    @pytest.fixture
    def write_queue_name(self):
        return "write_queue"

    @pytest.fixture
    def read_queue_name(self):
        return "read_queue"

    @pytest.fixture
    def callback_queue_name(self):
        return "callback_queue"

    @pytest.fixture
    def schema(self, mocker: MockFixture):
        return mocker.MagicMock()

    @pytest.fixture
    def super_init(self, mocker: MockFixture):
        return mocker.patch.object(BrokerHandler, "__init__", return_value=mocker.MagicMock())

    @pytest.fixture
    def loop_mock(self, mocker: MockFixture):
        return mocker.Mock(spec=asyncio.AbstractEventLoop)

    @pytest.fixture
    def get_running_loop_mock(self, loop_mock, mocker: MockFixture):
        return mocker.patch(
            "broker_grpc_lib.lib.rabbitmq_handler.asyncio.get_running_loop",
            return_value=loop_mock
        )

    @pytest.fixture
    def pool(self, mocker: MockFixture):
        return mocker.patch(
            "broker_grpc_lib.lib.rabbitmq_handler.Pool",
            return_value=mocker.Mock()
        )

    @pytest.fixture
    def get_connection(self, mocker: MockFixture):
        return mocker.patch.object(
            RabbitMQHandler, "_RabbitMQHandler__get_connection"
        )

    @pytest.fixture
    def get_channel(self, mocker: MockFixture):
        return mocker.patch.object(
            RabbitMQHandler, "_RabbitMQHandler__get_channel"
        )

    @pytest.fixture
    def init_pools(self, mocker: MockFixture):
        return mocker.patch.object(RabbitMQHandler, "_RabbitMQHandler__init_pools")

    @pytest.fixture
    def init_queues(self, mocker: MockFixture):
        return mocker.patch.object(RabbitMQHandler, "_RabbitMQHandler__init_queues")

    @pytest.fixture
    def handle_message(self, mocker: MockFixture):
        return mocker.patch.object(RabbitMQHandler, "_handle_message")

    @pytest.fixture
    def queue(self, message_obj, mocker: MockFixture):
        items = [message_obj, message_obj, message_obj]
        mock_iter = AsyncIterator(items)

        return mocker.MagicMock(
            publish=mocker.AsyncMock(),
            iterator=mocker.MagicMock(
                size=len(items),
                return_value=mocker.MagicMock(
                    __aenter__=mocker.AsyncMock(
                        return_value=mock_iter
                    )
                )
            )
        )

    @pytest.fixture
    def channel(self, queue, mocker: MockFixture):
        return mocker.MagicMock(
            declare_queue=mocker.AsyncMock(),
            get_queue=mocker.AsyncMock(return_value=queue)
        )

    @pytest.fixture
    def channel_pool(self, channel, mocker: MockFixture):
        return mocker.MagicMock(
            acquire=mocker.MagicMock(
                return_value=mocker.MagicMock(
                    __aenter__=mocker.AsyncMock(
                        return_value=channel
                    )
                )
            ),
            is_closed=False,
            close=mocker.AsyncMock()
        )

    @pytest.fixture
    def connection(self, channel, mocker: MockFixture):
        return mocker.MagicMock(
            channel=mocker.AsyncMock(return_value=channel)
        )

    @pytest.fixture
    def connection_pool(self, connection, mocker: MockFixture):
        return mocker.MagicMock(
            acquire=mocker.MagicMock(
                return_value=mocker.MagicMock(
                    __aenter__=mocker.AsyncMock(
                        return_value=connection
                    )
                )
            ),
            is_closed=False,
            close=mocker.AsyncMock()
        )

    @pytest.fixture
    def message_obj(self, mocker: MockFixture):
        return mocker.MagicMock(
            body='{"key_1": "val_1"}',
            process=mocker.MagicMock(
                return_value=mocker.MagicMock(
                    __aenter__=mocker.AsyncMock()
                )
            )
        )

    @pytest.fixture
    def message_cls(self, message_obj, mocker: MockFixture):
        return mocker.patch(
            "broker_grpc_lib.lib.rabbitmq_handler.Message",
            return_value=message_obj
        )

    @pytest.fixture
    def mock_iterator(self, message_obj, mocker: MockFixture):
        items = [message_obj, message_obj, message_obj, StopAsyncIteration]

        mock_iter = mocker.AsyncMock()
        mock_iter.__aiter__.return_value = mock_iter
        mock_iter.__anext__.side_effect = items
        mock_iter.size = len(items) - 1

        return mock_iter

    @pytest.fixture
    def validation_error(self, mocker: MockFixture):
        return mocker.patch("broker_grpc_lib.lib.rabbitmq_handler.ValidationError", new=Exception)

    @pytest.fixture
    def rpc_error(self, mocker: MockFixture):
        return mocker.patch("broker_grpc_lib.lib.rabbitmq_handler.grpc.RpcError", new=Exception)

    @pytest.fixture
    def no_write_queue_error(self, mocker: MockFixture):
        return mocker.patch("broker_grpc_lib.lib.rabbitmq_handler.NoWriteQueueException", new=Exception)

    @pytest.fixture
    def no_read_queue_error(self, mocker: MockFixture):
        return mocker.patch("broker_grpc_lib.lib.rabbitmq_handler.NoReadQueueException", new=Exception)

    @pytest.fixture
    def logging(self, mocker: MockFixture):
        return mocker.patch("broker_grpc_lib.lib.rabbitmq_handler.logging", return_value=mocker.MagicMock())

    @pytest.fixture
    def connect_robust(self, connection, mocker: MockFixture):
        return mocker.patch(
            "broker_grpc_lib.lib.rabbitmq_handler.aio_pika.connect_robust",
            return_value=mocker.AsyncMock(return_value=connection)
        )

    @pytest.fixture
    def rabbitmq_handler(
            self,
            rabbitmq_host,
            rabbitmq_login,
            rabbitmq_password,
            rabbitmq_port,
            grpc_stub,
            grpc_method_name,
            grpc_request_cls,
            schema,
            rabbitmq_max_connections,
            rabbitmq_max_channels,
            write_queue_name,
            read_queue_name,
            callback_queue_name,
            get_running_loop_mock,
            pool,
            channel_pool,
            connection_pool
    ):
        handler = RabbitMQHandler(
            rabbitmq_host, rabbitmq_login, rabbitmq_password, rabbitmq_port,
            grpc_stub, grpc_method_name, grpc_request_cls,
            schema,
            rabbitmq_max_connections, rabbitmq_max_channels,
            write_queue_name, read_queue_name, callback_queue_name
        )
        handler._channel_pool = channel_pool
        handler._connection_pool = connection_pool

        return handler

    def test_init_correct(
            self,
            rabbitmq_host,
            rabbitmq_login,
            rabbitmq_password,
            rabbitmq_port,
            grpc_stub,
            grpc_method_name,
            grpc_request_cls,
            schema,
            rabbitmq_max_connections,
            rabbitmq_max_channels,
            write_queue_name,
            read_queue_name,
            callback_queue_name,
            super_init,
            get_running_loop_mock,
            loop_mock
    ):
        handler = RabbitMQHandler(
            rabbitmq_host, rabbitmq_login, rabbitmq_password, rabbitmq_port,
            grpc_stub, grpc_method_name, grpc_request_cls,
            schema,
            rabbitmq_max_connections, rabbitmq_max_channels,
            write_queue_name, read_queue_name, callback_queue_name
        )
        super_init.assert_called_once_with(
            host=rabbitmq_host,
            login=rabbitmq_login,
            password=rabbitmq_password,
            port=rabbitmq_port,
            grpc_stub=grpc_stub,
            grpc_method_name=grpc_method_name,
            grpc_request_cls=grpc_request_cls,
            schema=schema
        )
        get_running_loop_mock.assert_called_once()
        assert handler._read_queue_name == read_queue_name
        assert handler._write_queue_name == write_queue_name
        assert handler._callback_queue_name == callback_queue_name
        assert handler._max_connections == rabbitmq_max_connections
        assert handler._max_channels == rabbitmq_max_channels
        assert handler._channel_pool is None
        assert handler._connection_pool is None
        assert handler._loop is loop_mock

    def test_init_assert_error(
            self,
            rabbitmq_host,
            rabbitmq_login,
            rabbitmq_password,
            rabbitmq_port,
            grpc_stub,
            grpc_method_name,
            grpc_request_cls,
            schema,
            rabbitmq_max_connections,
            rabbitmq_max_channels,
            super_init,
            get_running_loop_mock,
            loop_mock
    ):
        with pytest.raises(AssertionError):
            _ = RabbitMQHandler(
                rabbitmq_host, rabbitmq_login, rabbitmq_password, rabbitmq_port,
                grpc_stub, grpc_method_name, grpc_request_cls,
                schema,
                rabbitmq_max_connections, rabbitmq_max_channels,
                None, None, None
            )
        super_init.assert_called_once_with(
            host=rabbitmq_host,
            login=rabbitmq_login,
            password=rabbitmq_password,
            port=rabbitmq_port,
            grpc_stub=grpc_stub,
            grpc_method_name=grpc_method_name,
            grpc_request_cls=grpc_request_cls,
            schema=schema
        )
        get_running_loop_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_init_pools(
            self,
            rabbitmq_handler,
            pool,
            loop_mock,
            connection_pool,
            channel_pool,
            get_connection,
            get_channel,
            rabbitmq_max_connections,
            rabbitmq_max_channels,
            mocker: MockFixture
    ):
        pool.configure_mock(side_effect=[connection_pool, channel_pool])
        result = await rabbitmq_handler._RabbitMQHandler__init_pools()
        pool.assert_has_calls([
            mocker.call(get_connection, max_size=rabbitmq_max_connections, loop=loop_mock),
            mocker.call(get_channel, max_size=rabbitmq_max_channels, loop=loop_mock)
        ])
        assert result
        assert rabbitmq_handler._connection_pool is connection_pool
        assert rabbitmq_handler._channel_pool is channel_pool

    @pytest.mark.asyncio
    async def test_init_queues(
            self,
            rabbitmq_handler,
            read_queue_name,
            write_queue_name,
            callback_queue_name,
            rabbitmq_max_channels,
            channel_pool,
            channel,
            mocker: MockFixture
    ):
        result = await rabbitmq_handler._RabbitMQHandler__init_queues()

        assert channel_pool.acquire.call_count == rabbitmq_max_channels
        channel.declare_queue.assert_has_calls([
            mocker.call(read_queue_name),
            mocker.call(write_queue_name),
            mocker.call(callback_queue_name)
        ] * rabbitmq_max_channels)
        assert result

    @pytest.mark.asyncio
    async def test_prepare_handler(
            self,
            init_pools,
            init_queues,
            rabbitmq_handler
    ):
        init_queues.return_value = True
        init_pools.return_value = True

        result = await rabbitmq_handler.prepare_handler()

        init_pools.assert_called_once()
        init_queues.assert_called_once()
        assert result

    @pytest.mark.asyncio
    async def test_get_connection(
            self,
            rabbitmq_handler,
            connect_robust,
            rabbitmq_host,
            rabbitmq_login,
            rabbitmq_password,
            rabbitmq_port
    ):
        _ = await rabbitmq_handler._RabbitMQHandler__get_connection()
        connect_robust.assert_called_once_with(
            host=rabbitmq_host,
            login=rabbitmq_login,
            password=rabbitmq_password,
            port=rabbitmq_port
        )

    @pytest.mark.asyncio
    async def test_get_channel(
            self,
            connection_pool,
            connection,
            channel,
            rabbitmq_handler
    ):
        result = await rabbitmq_handler._RabbitMQHandler__get_channel()
        connection_pool.acquire.assert_called_once()
        connection.channel.assert_called_once()
        assert result is channel

    @pytest.mark.asyncio
    async def test_handle_message_correct(
            self,
            rabbitmq_handler,
            schema,
            grpc_method_name,
            grpc_request_cls,
            grpc_stub,
            message_obj,
            mocker: MockFixture
    ):
        grpc_request_cls.configure_mock(return_value=mocker.MagicMock(
            key_1="val_1"
        ))
        schema.configure_mock(
            parse_raw=mocker.MagicMock(
                return_value=mocker.MagicMock(
                    dict=mocker.MagicMock(
                        return_value={"key_1": "val_1"}
                    )
                )
            )
        )
        _ = await rabbitmq_handler._handle_message(message_obj)
        schema.parse_raw.assert_called_once_with(message_obj.body)
        schema.parse_raw.return_value.dict.assert_called_once_with(exclude_unset=True)
        grpc_request_cls.assert_called_once_with(key_1="val_1")
        grpc_stub.execute.assert_called_once_with(
            method_name=grpc_method_name,
            request=grpc_request_cls.return_value
        )

    @pytest.mark.asyncio
    async def test_handle_message_validation_error(
            self,
            rabbitmq_handler,
            schema,
            validation_error,
            grpc_method_name,
            grpc_request_cls,
            grpc_stub,
            logging,
            message_obj,
            mocker: MockFixture
    ):
        schema.configure_mock(
            parse_raw=mocker.MagicMock(
                side_effect=[Exception]
            )
        )

        _ = await rabbitmq_handler._handle_message(message_obj)

        schema.parse_raw.assert_called_once_with(message_obj.body)
        schema.parse_raw.return_value.dict.assert_not_called()
        grpc_request_cls.assert_not_called()
        grpc_stub.execute.assert_not_called()
        logging.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_message_rpc_error(
            self,
            rabbitmq_handler,
            schema,
            grpc_method_name,
            grpc_request_cls,
            grpc_stub,
            rpc_error,
            logging,
            message_obj,
            mocker: MockFixture
    ):
        grpc_request_cls.configure_mock(return_value=mocker.MagicMock(
            key_1="val_1"
        ))
        schema.configure_mock(
            parse_raw=mocker.MagicMock(
                return_value=mocker.MagicMock(
                    dict=mocker.MagicMock(
                        return_value={"key_1": "val_1"}
                    )
                )
            )
        )
        grpc_stub.configure_mock(execute=mocker.AsyncMock(side_effect=[Exception]))

        _ = await rabbitmq_handler._handle_message(message_obj)

        schema.parse_raw.assert_called_once_with(message_obj.body)
        schema.parse_raw.return_value.dict.assert_called_once_with(exclude_unset=True)
        grpc_request_cls.assert_called_once()
        grpc_stub.execute.assert_called_once()
        logging.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_message_correct(
            self,
            write_queue_name,
            rabbitmq_handler,
            message_obj,
            message_cls,
            queue,
            channel,
            channel_pool
    ):
        message_body = "{'key_1': 'val_1'}".encode()
        _ = await rabbitmq_handler.write_message(message_body)
        channel_pool.acquire.assert_called_once()
        channel.get_queue.assert_called_once_with(write_queue_name)
        message_cls.assert_called_once_with(body=message_body)
        queue.publish.assert_called_once_with(message_obj)

    @pytest.mark.asyncio
    async def test_write_message_no_queue(
            self,
            no_write_queue_error,
            write_queue_name,
            rabbitmq_handler,
            message_obj,
            message_cls,
            queue,
            channel,
            channel_pool
    ):
        rabbitmq_handler._write_queue_name = None
        message_body = "{'key_1': 'val_1'}".encode()

        with pytest.raises(Exception):
            _ = await rabbitmq_handler.write_message(message_body)
        channel_pool.acquire.assert_not_called()
        channel.get_queue.assert_not_called()
        message_cls.assert_not_called()
        queue.publish.assert_not_called()

    @pytest.mark.asyncio
    async def test_start_correct(
            self,
            rabbitmq_handler,
            channel,
            channel_pool,
            read_queue_name,
            queue,
            message_obj,
            handle_message,
            mocker: MockFixture
    ):
        _ = await rabbitmq_handler.start()
        channel_pool.acquire.assert_called_once()
        channel.get_queue.assert_called_once_with(read_queue_name)
        queue.iterator.assert_called_once()
        call_count = queue.iterator.size
        assert message_obj.process.call_count == call_count
        handle_message.assert_has_calls([mocker.call(message_obj)]*call_count)

    @pytest.mark.asyncio
    async def test_start_no_queue(
            self,
            rabbitmq_handler,
            channel_pool,
            handle_message,
            queue,
            channel,
            message_obj,
            no_read_queue_error
    ):
        rabbitmq_handler._read_queue_name = None

        with pytest.raises(Exception):
            _ = await rabbitmq_handler.start()

        channel_pool.acquire.assert_not_called()
        queue.iterator.assert_not_called()
        message_obj.assert_not_called()
        handle_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_stop(
            self,
            connection_pool,
            channel_pool,
            rabbitmq_handler,
            logging
    ):
        await rabbitmq_handler.stop()

        connection_pool.close.assert_called_once()
        channel_pool.close.assert_called_once()
        logging.info.assert_called_once()
