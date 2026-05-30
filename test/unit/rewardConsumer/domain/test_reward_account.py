from src.rewardConsumer.domain.reward import Reward
from src.rewardConsumer.domain.reward_account import RewardAccount


class TestRewardAccount:
    def test_new_account_starts_at_zero(self):
        account = RewardAccount(card_number="4000-0000-0000-0000")
        assert account.total_points == 0.0
        assert account.total_cashback == 0.0

    def test_add_reward_updates_totals(self):
        account = RewardAccount(card_number="4000-0000-0000-0000")
        reward = Reward(points=500.0, cashback=25.0)
        account.add_reward(reward)
        assert account.total_points == 500.0
        assert account.total_cashback == 25.0

    def test_multiple_rewards_accumulate(self):
        account = RewardAccount(card_number="4000-0000-0000-0000")
        account.add_reward(Reward(points=100.0, cashback=5.0))
        account.add_reward(Reward(points=200.0, cashback=10.0))
        assert account.total_points == 300.0
        assert account.total_cashback == 15.0
