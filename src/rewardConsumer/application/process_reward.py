from src.rewardConsumer.domain.reward import Reward
from src.rewardConsumer.domain.reward_account import RewardAccount
from src.rewardConsumer.application.ports import RewardRepositoryPort


class ProcessRewardUseCase:
    def __init__(self, repository: RewardRepositoryPort):
        self._repository = repository

    def execute(self, amount: float, card_number: str, restaurant_code: str) -> Reward:
        account = self._repository.find_by_card(card_number)
        if account is None:
            account = RewardAccount(card_number=card_number)

        reward = Reward.calculate(amount)
        account.add_reward(reward)
        self._repository.save(account)

        print(f"[✓] Recompensa para {card_number}: {reward.points} pts, S/{reward.cashback:.2f} cashback")
        return reward
