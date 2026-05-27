from unittest.mock import patch

from fastapi.testclient import TestClient


class TestAPI:
    @patch("src.costumerProducer.infraestructure.api.RabbitMQAdapter")
    def test_register_transaction_ok(self, mock_adapter_cls):
        from src.costumerProducer.infraestructure.api import app
        client = TestClient(app)

        response = client.post("/transactions", json={
            "amount": 150.0,
            "card_number": "4000-1234-5678-9012",
            "restaurant_code": "REST-001",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Cena registrada exitosamente"
        assert data["amount"] == 150.0
        assert data["card_number"] == "4000-1234-5678-9012"
        assert data["restaurant_code"] == "REST-001"
        assert "date_time" in data
        mock_adapter_cls.assert_called_once()

    @patch("src.costumerProducer.infraestructure.api.RabbitMQAdapter")
    def test_register_transaction_invalid_amount(self, mock_adapter_cls):
        from src.costumerProducer.infraestructure.api import app
        client = TestClient(app)

        response = client.post("/transactions", json={
            "amount": -10,
            "card_number": "4000-1234-5678-9012",
            "restaurant_code": "REST-001",
        })

        assert response.status_code == 400
        assert response.json()["detail"] == "El monto debe ser mayor a 0"
        mock_adapter_cls.assert_not_called()

    @patch("src.costumerProducer.infraestructure.api.RabbitMQAdapter")
    def test_health(self, mock_adapter_cls):
        from src.costumerProducer.infraestructure.api import app
        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
