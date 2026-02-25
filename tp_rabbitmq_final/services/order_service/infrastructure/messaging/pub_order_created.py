import pika
import json
import time
from services.order_service.domain.events import ORDER_CREATED, ORDERLINE_CREATED


class OrderEventEmitter:
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

    def emit_order_created(self, order_data: dict):
        self._ensure_connection()
        self._channel.basic_publish(
            exchange="events",
            routing_key=ORDER_CREATED,
            body=json.dumps(order_data),
        )

    def emit_orderline_created(self, line_data: dict):
        self._ensure_connection()
        self._channel.basic_publish(
            exchange="events",
            routing_key=ORDERLINE_CREATED,
            body=json.dumps(line_data),
        )
