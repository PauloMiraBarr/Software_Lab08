from pytest import approx

from src.rewardConsumer.domain.reward import Reward


class TestReward:
    def test_calculate_returns_points_and_cashback(self):
        reward = Reward.calculate(100.0)
        assert reward.points == 1000.0
        assert reward.cashback == 5.0

    def test_calculate_zero_amount(self):
        reward = Reward.calculate(0.0)
        assert reward.points == 0.0
        assert reward.cashback == 0.0

    def test_calculate_round_values(self):
        reward = Reward.calculate(33.33)
        assert reward.points == approx(333.3)
        assert reward.cashback == approx(1.6665)
