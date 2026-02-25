import pika
import json
import uuid
import time


class InventoryPairClient:
    def __init__(self, rabbitmq_host: str = "rabbitmq"):
        self._host = rabbitmq_host
        self._conn = None
        self._channel = None
        self._reply_queue = None
        self._response = None
        self._corr_id = None

    def _ensure_connection(self):
        if self._conn and self._conn.is_open:
            return
        for _ in range(10):
            try:
                self._conn = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self._host)
                )
                self._channel = self._conn.channel()
                result = self._channel.queue_declare(queue="", exclusive=True)
                self._reply_queue = result.method.queue
                self._channel.basic_consume(
                    queue=self._reply_queue,
                    on_message_callback=self._on_reply,
                    auto_ack=True,
                )
                return
            except pika.exceptions.AMQPConnectionError:
                time.sleep(2)
        raise RuntimeError("Connexion RabbitMQ impossible")

    def _on_reply(self, ch, method, props, body):
        if self._corr_id == props.correlation_id:
            self._response = json.loads(body)

    def fetch_stock(self, product_id: str) -> dict:
        self._ensure_connection()
        self._response = None
        self._corr_id = str(uuid.uuid4())
        message = {"action": "get_inventory_by_product", "data": {"product_id": product_id}}
        self._channel.basic_publish(
            exchange="",
            routing_key="inventory_queue",
            properties=pika.BasicProperties(
                reply_to=self._reply_queue,
                correlation_id=self._corr_id,
            ),
            body=json.dumps(message),
        )
        try:
            self._conn.process_data_events(time_limit=5)
        except Exception:
            pass
        return self._response or {}
