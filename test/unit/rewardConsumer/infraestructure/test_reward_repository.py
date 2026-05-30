from src.rewardConsumer.domain.reward_account import RewardAccount
from src.rewardConsumer.infraestructure.reward_repository import InMemoryRewardRepository


class TestInMemoryRewardRepository:
    def test_save_and_find(self):
        repo = InMemoryRewardRepository()
        account = RewardAccount(card_number="4000-0000-0000-0000", total_points=100.0, total_cashback=5.0)
        repo.save(account)
        found = repo.find_by_card("4000-0000-0000-0000")
        assert found is account

    def test_find_nonexistent_returns_none(self):
        repo = InMemoryRewardRepository()
        assert repo.find_by_card("no-existe") is None

    def test_save_overwrites_existing(self):
        repo = InMemoryRewardRepository()
        account = RewardAccount(card_number="4000-0000-0000-0000", total_points=100.0, total_cashback=5.0)
        repo.save(account)

        updated = RewardAccount(card_number="4000-0000-0000-0000", total_points=200.0, total_cashback=10.0)
        repo.save(updated)

        found = repo.find_by_card("4000-0000-0000-0000")
        assert found.total_points == 200.0
