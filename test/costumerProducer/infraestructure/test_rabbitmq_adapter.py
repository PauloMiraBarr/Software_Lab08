import json
from datetime import datetime
from unittest.mock import MagicMock

from src.costumerProducer.domain.dinner_transaction import DinnerTransaction
from src.costumerProducer.infraestructure.rabbitmq_adapter import RabbitMQAdapter


class TestRabbitMQAdapter:
    def test_publish_sends_json_message(self):
        mock_conn = MagicMock()
        mock_conn.queue = "test-queue"
        adapter = RabbitMQAdapter(connection=mock_conn)
        tx = DinnerTransaction(
            amount=100.0,
            card_number="4000-1111-2222-3333",
            restaurant_code="REST-001",
            date_time=datetime(2024, 5, 20, 12, 30, 0),
        )

        adapter.publish(tx)

        mock_conn.channel.basic_publish.assert_called_once()
        _, kwargs = mock_conn.channel.basic_publish.call_args
        assert kwargs["exchange"] == ""
        assert kwargs["routing_key"] == "test-queue"

        body = json.loads(kwargs["body"])
        assert body["amount"] == 100.0
        assert body["card_number"] == "4000-1111-2222-3333"
        assert body["restaurant_code"] == "REST-001"
        assert body["date_time"] == "2024-05-20T12:30:00"

    def test_close_connection(self):
        mock_conn = MagicMock()
        adapter = RabbitMQAdapter(connection=mock_conn)
        adapter.close()
        mock_conn.close.assert_called_once()
