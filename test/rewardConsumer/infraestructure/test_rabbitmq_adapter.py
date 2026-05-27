import json
from unittest.mock import MagicMock, Mock

from src.rewardConsumer.infraestructure.rabbitmq_adapter import RabbitMQConsumerAdapter


class TestRabbitMQConsumerAdapter:
    def test_callback_calls_use_case(self):
        mock_conn = MagicMock()
        use_case = Mock()
        adapter = RabbitMQConsumerAdapter(use_case, connection=mock_conn)
        body = json.dumps({
            "amount": 250.0,
            "card_number": "4111-1111-1111-1111",
            "restaurant_code": "REST-002",
            "date_time": "2024-05-20T12:30:00",
        }).encode()

        adapter._callback(None, None, None, body)

        use_case.execute.assert_called_once_with(250.0, "4111-1111-1111-1111", "REST-002")

    def test_start_consuming(self):
        mock_conn = MagicMock()
        mock_conn.queue = "test-queue"
        use_case = Mock()
        adapter = RabbitMQConsumerAdapter(use_case, connection=mock_conn)

        adapter.start()

        mock_conn.channel.basic_consume.assert_called_once()
        mock_conn.channel.start_consuming.assert_called_once()

    def test_close_connection(self):
        mock_conn = MagicMock()
        use_case = Mock()
        adapter = RabbitMQConsumerAdapter(use_case, connection=mock_conn)
        adapter.close()
        mock_conn.close.assert_called_once()
