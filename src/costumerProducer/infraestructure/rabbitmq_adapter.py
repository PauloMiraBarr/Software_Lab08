import json
from datetime import datetime

import pika

from src.costumerProducer.application.ports import MessageBrokerPort
from src.costumerProducer.domain.dinner_transaction import DinnerTransaction
from src.rabbitService.infraestructure.connection import RabbitMQConnection


class RabbitMQAdapter(MessageBrokerPort):
    def __init__(self, connection: RabbitMQConnection | None = None):
        self._conn = connection or RabbitMQConnection()

    def publish(self, transaction: DinnerTransaction) -> None:
        message = {
            "amount": transaction.amount,
            "card_number": transaction.card_number,
            "restaurant_code": transaction.restaurant_code,
            "date_time": transaction.date_time.isoformat(),
        }
        self._conn.channel.basic_publish(
            exchange="",
            routing_key=self._conn.queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self) -> None:
        self._conn.close()
