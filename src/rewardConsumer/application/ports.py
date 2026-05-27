from abc import ABC, abstractmethod

from src.rewardConsumer.domain.reward_account import RewardAccount


class RewardRepositoryPort(ABC):
    @abstractmethod
    def find_by_card(self, card_number: str) -> RewardAccount | None:
        pass

    @abstractmethod
    def save(self, account: RewardAccount) -> None:
        pass
