import json

from fastapi.testclient import TestClient


class TestAPIIntegration:
    def test_register_transaction_sends_to_queue(self, rabbitmq_env):
        from src.costumerProducer.infraestructure.api import app
        client = TestClient(app)

        response = client.post("/transactions", json={
            "amount": 200.0,
            "card_number": "5000-1111-2222-3333",
            "restaurant_code": "REST-API",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["amount"] == 200.0

        from src.rabbitService.infraestructure.connection import RabbitMQConnection
        conn = RabbitMQConnection()
        method, properties, body = conn.channel.basic_get(
            queue=conn.queue, auto_ack=True
        )

        assert method is not None, "No message in queue"
        payload = json.loads(body.decode())
        assert payload["amount"] == 200.0
        assert payload["card_number"] == "5000-1111-2222-3333"
        assert payload["restaurant_code"] == "REST-API"
        assert "date_time" in payload

        conn.close()

    def test_invalid_amount_does_not_publish(self, rabbitmq_env):
        from src.costumerProducer.infraestructure.api import app
        client = TestClient(app)

        response = client.post("/transactions", json={
            "amount": -10,
            "card_number": "5000-1111-2222-3333",
            "restaurant_code": "REST-API",
        })

        assert response.status_code == 400
        assert "mayor a 0" in response.json()["detail"]

        from src.rabbitService.infraestructure.connection import RabbitMQConnection
        conn = RabbitMQConnection()
        method, properties, body = conn.channel.basic_get(queue=conn.queue)
        assert method is None, "Message should not be in queue for invalid amount"
        conn.close()

    def test_health_endpoint(self, rabbitmq_env):
        from src.costumerProducer.infraestructure.api import app
        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
