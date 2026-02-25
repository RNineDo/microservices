import pika
import json
import uuid
import os
import time


class OrderRequester:
    QUEUE_NAME = "order_queue"

    def __init__(self):
        self._host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self._conn = None
        self._channel = None
        self._reply_queue = None
        self._response = None
        self._corr_id = None

    def _ensure_connection(self):
        if self._conn and self._conn.is_open:
            return
        for attempt in range(10):
            try:
                self._conn = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self._host)
                )
                self._channel = self._conn.channel()
                result = self._channel.queue_declare(queue="", exclusive=True)
                self._reply_queue = result.method.queue
                self._channel.basic_consume(
                    queue=self._reply_queue,
                    on_message_callback=self._handle_reply,
                    auto_ack=True,
                )
                return
            except pika.exceptions.AMQPConnectionError:
                time.sleep(2)
        raise RuntimeError("Impossible de se connecter a RabbitMQ")

    def _handle_reply(self, ch, method, props, body):
        if self._corr_id == props.correlation_id:
            self._response = json.loads(body)

    def send(self, action: str, data: dict = None) -> dict:
        self._ensure_connection()
        self._response = None
        self._corr_id = str(uuid.uuid4())
        message = {"action": action, "data": data or {}}
        self._channel.basic_publish(
            exchange="",
            routing_key=self.QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=self._reply_queue,
                correlation_id=self._corr_id,
            ),
            body=json.dumps(message),
        )
        while self._response is None:
            self._conn.process_data_events(time_limit=30)
        return self._response
