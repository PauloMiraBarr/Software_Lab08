from abc import ABC, abstractmethod
from src.costumerProducer.domain.dinner_transaction import DinnerTransaction


class MessageBrokerPort(ABC):
    @abstractmethod
    def publish(self, transaction: DinnerTransaction) -> None:
        pass
