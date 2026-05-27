import os

import pika
from dotenv import load_dotenv

load_dotenv()


class RabbitMQConnection:
    def __init__(self):
        credentials = pika.PlainCredentials(
            os.getenv("RABBITMQ_USER"),
            os.getenv("RABBITMQ_PASS"),
        )
        parameters = pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT")),
            virtual_host=os.getenv("RABBITMQ_VHOST"),
            credentials=credentials,
        )
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._queue = os.getenv("RABBITMQ_QUEUE")
        self._channel.queue_declare(queue=self._queue, durable=True)

    @property
    def channel(self):
        return self._channel

    @property
    def queue(self):
        return self._queue

    def close(self):
        self._connection.close()
