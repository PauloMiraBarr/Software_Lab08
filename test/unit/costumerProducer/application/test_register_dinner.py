from datetime import datetime
from unittest.mock import Mock

from src.costumerProducer.application.register_dinner import RegisterDinnerUseCase
from src.costumerProducer.domain.dinner_transaction import DinnerTransaction


class TestRegisterDinnerUseCase:
    def test_execute_publishes_transaction(self):
        broker = Mock()
        use_case = RegisterDinnerUseCase(broker)

        tx = DinnerTransaction(
            amount=200.0,
            card_number="4111-1111-1111-1111",
            restaurant_code="REST-003",
            date_time=datetime.now(),
        )

        use_case.execute(tx)

        broker.publish.assert_called_once_with(tx)
