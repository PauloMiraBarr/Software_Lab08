import json
from datetime import datetime

from src.costumerProducer.domain.dinner_transaction import DinnerTransaction
from src.costumerProducer.infraestructure.rabbitmq_adapter import RabbitMQAdapter
from src.rewardConsumer.application.process_reward import ProcessRewardUseCase
from src.rewardConsumer.infraestructure.reward_repository import InMemoryRewardRepository


class TestFullPipeline:
    def test_publish_and_consume_message(self, rabbitmq_connection):
        adapter = RabbitMQAdapter(connection=rabbitmq_connection)
        repo = InMemoryRewardRepository()
        use_case = ProcessRewardUseCase(repo)

        tx = DinnerTransaction(
            amount=100.0,
            card_number="4000-1111-2222-3333",
            restaurant_code="REST-001",
            date_time=datetime(2025, 5, 29, 10, 0, 0),
        )
        adapter.publish(tx)

        method, properties, body = rabbitmq_connection.channel.basic_get(
            queue=rabbitmq_connection.queue, auto_ack=True
        )
        assert method is not None, "No message in queue"

        data = json.loads(body.decode())
        assert data["amount"] == 100.0
        assert data["card_number"] == "4000-1111-2222-3333"
        assert data["restaurant_code"] == "REST-001"
        assert data["date_time"] == "2025-05-29T10:00:00"

        reward = use_case.execute(data["amount"], data["card_number"], data["restaurant_code"])
        assert reward.points == 1000.0
        assert reward.cashback == 5.0

        account = repo.find_by_card("4000-1111-2222-3333")
        assert account.total_points == 1000.0
        assert account.total_cashback == 5.0

    def test_multiple_transactions_accumulate(self, rabbitmq_connection):
        adapter = RabbitMQAdapter(connection=rabbitmq_connection)
        repo = InMemoryRewardRepository()
        use_case = ProcessRewardUseCase(repo)

        for amount in [50.0, 150.0]:
            tx = DinnerTransaction(
                amount=amount,
                card_number="4000-1111-2222-4444",
                restaurant_code="REST-002",
                date_time=datetime.now(),
            )
            adapter.publish(tx)

        for _ in range(2):
            method, properties, body = rabbitmq_connection.channel.basic_get(
                queue=rabbitmq_connection.queue, auto_ack=True
            )
            assert method is not None
            data = json.loads(body.decode())
            use_case.execute(data["amount"], data["card_number"], data["restaurant_code"])

        account = repo.find_by_card("4000-1111-2222-4444")
        assert account.total_points == 2000.0
        assert account.total_cashback == 10.0

    def test_publish_via_adapter_then_consumer_callback(self, rabbitmq_connection):
        from src.rewardConsumer.infraestructure.rabbitmq_adapter import RabbitMQConsumerAdapter

        adapter = RabbitMQAdapter(connection=rabbitmq_connection)
        repo = InMemoryRewardRepository()
        use_case = ProcessRewardUseCase(repo)
        consumer = RabbitMQConsumerAdapter(use_case, connection=rabbitmq_connection)

        tx = DinnerTransaction(
            amount=75.0,
            card_number="4000-1111-2222-5555",
            restaurant_code="REST-003",
            date_time=datetime.now(),
        )
        adapter.publish(tx)

        method, properties, body = rabbitmq_connection.channel.basic_get(
            queue=rabbitmq_connection.queue, auto_ack=True
        )
        assert method is not None, "No message in queue"

        consumer._callback(None, method, properties, body)

        account = repo.find_by_card("4000-1111-2222-5555")
        assert account is not None
        assert account.total_points == 750.0
        assert account.total_cashback == 3.75

        # connection is closed by the fixture, no need to call adapter/consumer.close()

    def test_empty_queue_returns_none(self, rabbitmq_connection):
        method, properties, body = rabbitmq_connection.channel.basic_get(
            queue=rabbitmq_connection.queue
        )
        assert method is None
