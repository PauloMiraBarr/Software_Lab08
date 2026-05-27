from unittest.mock import patch

from src.rabbitService.infraestructure.connection import RabbitMQConnection


class TestRabbitMQConnection:
    def test_constructor_creates_channel_and_queue(self):
        with patch("src.rabbitService.infraestructure.connection.pika") as mock_pika:
            conn = RabbitMQConnection()
            mock_pika.PlainCredentials.assert_called_once()
            mock_pika.ConnectionParameters.assert_called_once()
            mock_pika.BlockingConnection.assert_called_once()
            conn.channel.queue_declare.assert_called_once()

    def test_channel_property(self):
        with patch("src.rabbitService.infraestructure.connection.pika") as mock_pika:
            conn = RabbitMQConnection()
            assert conn.channel is conn._channel

    def test_queue_property(self):
        with patch("src.rabbitService.infraestructure.connection.pika") as mock_pika:
            conn = RabbitMQConnection()
            assert conn.queue == conn._queue

    def test_close(self):
        with patch("src.rabbitService.infraestructure.connection.pika") as mock_pika:
            conn = RabbitMQConnection()
            conn.close()
            conn._connection.close.assert_called_once()
