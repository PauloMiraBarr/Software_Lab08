from dataclasses import dataclass, field

from src.rewardConsumer.domain.reward import Reward


@dataclass
class RewardAccount:
    card_number: str
    total_points: float = 0.0
    total_cashback: float = 0.0

    def add_reward(self, reward: Reward) -> None:
        self.total_points += reward.points
        self.total_cashback += reward.cashback
