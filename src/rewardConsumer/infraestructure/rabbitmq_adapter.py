import json

from src.rabbitService.infraestructure.connection import RabbitMQConnection
from src.rewardConsumer.application.process_reward import ProcessRewardUseCase


class RabbitMQConsumerAdapter:
    def __init__(self, use_case: ProcessRewardUseCase, connection: RabbitMQConnection | None = None):
        self._use_case = use_case
        self._conn = connection or RabbitMQConnection()

    def _callback(self, ch, method, properties, body):
        data = json.loads(body.decode())
        self._use_case.execute(data["amount"], data["card_number"], data["restaurant_code"])

    def start(self) -> None:
        print(f"[*] Esperando transacciones en {self._conn.queue}")
        self._conn.channel.basic_consume(
            queue=self._conn.queue,
            on_message_callback=self._callback,
            auto_ack=True,
        )
        self._conn.channel.start_consuming()

    def close(self) -> None:
        self._conn.close()
