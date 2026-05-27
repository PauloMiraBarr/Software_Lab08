import argparse
from datetime import datetime

import uvicorn

from src.costumerProducer.application.register_dinner import RegisterDinnerUseCase
from src.costumerProducer.domain.dinner_transaction import DinnerTransaction
from src.costumerProducer.infraestructure.rabbitmq_adapter import RabbitMQAdapter
from src.rewardConsumer.application.process_reward import ProcessRewardUseCase
from src.rewardConsumer.infraestructure.rabbitmq_adapter import RabbitMQConsumerAdapter
from src.rewardConsumer.infraestructure.reward_repository import InMemoryRewardRepository


def _cmd_produce(amount: float, card_number: str, restaurant_code: str):
    transaction = DinnerTransaction(
        amount=amount,
        card_number=card_number,
        restaurant_code=restaurant_code,
        date_time=datetime.now(),
    )
    adapter = RabbitMQAdapter()
    use_case = RegisterDinnerUseCase(adapter)
    use_case.execute(transaction)
    print(f"[x] Cena registrada: S/{transaction.amount} en {transaction.restaurant_code}")
    adapter.close()


def _cmd_consume():
    repository = InMemoryRewardRepository()
    use_case = ProcessRewardUseCase(repository)
    consumer = RabbitMQConsumerAdapter(use_case)
    try:
        consumer.start()
    except KeyboardInterrupt:
        consumer.close()


def _cmd_serve(port: int):
    uvicorn.run("src.costumerProducer.infraestructure.api:app", host="127.0.0.1", port=port)


def main():
    parser = argparse.ArgumentParser(description="Sistema de Recompensas - EDA")
    sub = parser.add_subparsers(dest="command", required=True)

    p_produce = sub.add_parser("produce", help="Publicar evento de cena")
    p_produce.add_argument("--amount", type=float, default=150.0)
    p_produce.add_argument("--card", type=str, default="4000-1234-5678-9012")
    p_produce.add_argument("--restaurant", type=str, default="REST-001")

    sub.add_parser("consume", help="Iniciar consumidor de recompensas")

    p_serve = sub.add_parser("serve", help="Iniciar API REST")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.command == "produce":
        _cmd_produce(amount=args.amount, card_number=args.card, restaurant_code=args.restaurant)
    elif args.command == "consume":
        _cmd_consume()
    elif args.command == "serve":
        _cmd_serve(args.port)


if __name__ == "__main__":
    main()
