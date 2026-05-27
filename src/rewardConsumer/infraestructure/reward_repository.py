from src.rewardConsumer.application.ports import RewardRepositoryPort
from src.rewardConsumer.domain.reward_account import RewardAccount


class InMemoryRewardRepository(RewardRepositoryPort):
    def __init__(self):
        self._accounts: dict[str, RewardAccount] = {}

    def find_by_card(self, card_number: str) -> RewardAccount | None:
        return self._accounts.get(card_number)

    def save(self, account: RewardAccount) -> None:
        self._accounts[account.card_number] = account
