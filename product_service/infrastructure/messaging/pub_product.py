import pika
import json
import time
from services.product_service.domain.events import PRODUCT_CREATED


class ProductEventEmitter:
    def __init__(self, rabbitmq_host: str = "rabbitmq"):
        self._host = rabbitmq_host
        self._conn = None
        self._channel = None

    def _ensure_connection(self):
        if self._conn and self._conn.is_open:
            return
        for _ in range(10):
            try:
                self._conn = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self._host)
                )
                self._channel = self._conn.channel()
                self._channel.exchange_declare(exchange="events", exchange_type="topic")
                return
            except pika.exceptions.AMQPConnectionError:
                time.sleep(2)
        raise RuntimeError("Connexion RabbitMQ impossible")

    def emit_created(self, product_data: dict):
        self._ensure_connection()
        self._channel.basic_publish(
            exchange="events",
            routing_key=PRODUCT_CREATED,
            body=json.dumps(product_data),
        )
