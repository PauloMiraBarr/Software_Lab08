import os
import uuid

import pytest
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="session")
def rabbitmq_container():
    with RabbitMqContainer("rabbitmq:3-management") as container:
        yield container


@pytest.fixture
def rabbitmq_env(rabbitmq_container):
    queue = f"test-queue-{uuid.uuid4().hex[:8]}"
    env = {
        "RABBITMQ_HOST": rabbitmq_container.get_container_host_ip(),
        "RABBITMQ_PORT": str(rabbitmq_container.get_exposed_port(rabbitmq_container.port)),
        "RABBITMQ_USER": rabbitmq_container.username,
        "RABBITMQ_PASS": rabbitmq_container.password,
        "RABBITMQ_VHOST": rabbitmq_container.vhost,
        "RABBITMQ_QUEUE": queue,
    }

    saved = {k: os.environ.get(k) for k in env}
    for k, v in env.items():
        os.environ[k] = v

    yield env

    for k in env:
        if saved[k] is not None:
            os.environ[k] = saved[k]
        else:
            os.environ.pop(k, None)


@pytest.fixture
def rabbitmq_connection(rabbitmq_env):
    from src.rabbitService.infraestructure.connection import RabbitMQConnection
    conn = RabbitMQConnection()
    yield conn
    try:
        conn.close()
    except Exception:
        pass
