import pytest
from pytest_mock import MockFixture

from broker_grpc_lib.lib.grpc_client import GRPCClient


class TestGRPCClient:

    @pytest.fixture
    def channel_mock(self, mocker: MockFixture):
        return mocker.MagicMock(
            close=mocker.AsyncMock()
        )

    @pytest.fixture
    def insecure_channel_mock(self, channel_mock, mocker: MockFixture):
        return mocker.patch(
            "broker_grpc_lib.lib.grpc_client.grpc.aio.insecure_channel",
            return_value=channel_mock
        )

    @pytest.fixture
    def grpc_stub_mock(self, mocker: MockFixture):
        stub = mocker.MagicMock(return_value=mocker.AsyncMock())
        method = mocker.AsyncMock(return_value="result")
        stub.return_value.method = method

        return stub

    @pytest.fixture
    def grpc_host(self):
        return "localhost"

    @pytest.fixture
    def grpc_port(self):
        return 57775

    @pytest.fixture
    def client_mock(
            self,
            grpc_stub_mock,
            insecure_channel_mock,
            channel_mock,
            grpc_host,
            grpc_port
    ):
        return GRPCClient(stub_cls=grpc_stub_mock, grpc_host=grpc_host, grpc_port=grpc_port)

    def test_init(
            self,
            client_mock,
            grpc_port,
            grpc_host,
            insecure_channel_mock,
            channel_mock,
            grpc_stub_mock
    ):
        insecure_channel_mock.assert_called_once_with(f"{grpc_host}:{grpc_port}")
        grpc_stub_mock.assert_called_once_with(channel_mock)

    @pytest.mark.asyncio
    async def test_execute(
            self,
            client_mock,
            grpc_stub_mock,
            mocker: MockFixture
    ):
        request = mocker.MagicMock(key="value")
        method_name = "method"
        result = await client_mock.execute(method_name=method_name, request=request)
        grpc_stub_mock.return_value.method.assert_called_once_with(request)
        assert result == grpc_stub_mock.return_value.method.return_value

    @pytest.mark.asyncio
    async def test_cleanup(
            self,
            channel_mock,
            client_mock
    ):
        _ = await client_mock.cleanup()
        channel_mock.close.assert_called_once()
