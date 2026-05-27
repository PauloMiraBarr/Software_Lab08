from src.costumerProducer.domain.dinner_transaction import DinnerTransaction
from src.costumerProducer.application.ports import MessageBrokerPort


class RegisterDinnerUseCase:
    def __init__(self, broker: MessageBrokerPort):
        self._broker = broker

    def execute(self, transaction: DinnerTransaction) -> None:
        self._broker.publish(transaction)
