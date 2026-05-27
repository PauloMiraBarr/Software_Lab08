from datetime import datetime

from src.costumerProducer.domain.dinner_transaction import DinnerTransaction


class TestDinnerTransaction:
    def test_create_transaction(self):
        now = datetime.now()
        tx = DinnerTransaction(
            amount=150.00,
            card_number="4000-1234-5678-9012",
            restaurant_code="REST-001",
            date_time=now,
        )
        assert tx.amount == 150.00
        assert tx.card_number == "4000-1234-5678-9012"
        assert tx.restaurant_code == "REST-001"
        assert tx.date_time == now

    def test_transaction_is_immutable(self):
        from dataclasses import FrozenInstanceError
        tx = DinnerTransaction(
            amount=50.0,
            card_number="1234",
            restaurant_code="REST-002",
            date_time=datetime.now(),
        )
        with pytest.raises(FrozenInstanceError):
            tx.amount = 999.0


import pytest
