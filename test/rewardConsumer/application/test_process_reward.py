from unittest.mock import Mock

from src.rewardConsumer.application.process_reward import ProcessRewardUseCase
from src.rewardConsumer.domain.reward_account import RewardAccount


class TestProcessRewardUseCase:
    def test_execute_creates_account_and_returns_reward(self):
        repository = Mock()
        repository.find_by_card.return_value = None
        use_case = ProcessRewardUseCase(repository)

        reward = use_case.execute(100.0, "4000-0000-0000-0000", "REST-001")

        assert reward.points == 1000.0
        assert reward.cashback == 5.0
        repository.save.assert_called_once()
        saved = repository.save.call_args[0][0]
        assert saved.card_number == "4000-0000-0000-0000"
        assert saved.total_points == 1000.0
        assert saved.total_cashback == 5.0

    def test_execute_updates_existing_account(self):
        repository = Mock()
        existing = RewardAccount(card_number="4000-0000-0000-0000", total_points=500.0, total_cashback=25.0)
        repository.find_by_card.return_value = existing
        use_case = ProcessRewardUseCase(repository)

        reward = use_case.execute(50.0, "4000-0000-0000-0000", "REST-001")

        assert reward.points == 500.0
        assert reward.cashback == 2.5
        repository.save.assert_called_once_with(existing)
        assert existing.total_points == 1000.0
        assert existing.total_cashback == 27.5
