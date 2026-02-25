import pika
import json
import time


class GatewayResponder:
    QUEUE_NAME = "order_queue"

    def __init__(self, handler_func, rabbitmq_host: str = "rabbitmq"):
        self._handler = handler_func
        self._host = rabbitmq_host

    def start_listening(self):
        for _ in range(15):
            try:
                conn = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self._host)
                )
                channel = conn.channel()
                channel.queue_declare(queue=self.QUEUE_NAME)
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(
                    queue=self.QUEUE_NAME,
                    on_message_callback=self._process_request,
                )
                print(f"[OrderService] En ecoute sur {self.QUEUE_NAME}")
                channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                print("[OrderService] RabbitMQ pas encore pret, nouvelle tentative...")
                time.sleep(3)
        raise RuntimeError("Impossible de demarrer le consommateur RPC")

    def _process_request(self, ch, method, props, body):
        message = json.loads(body)
        action = message.get("action")
        data = message.get("data", {})
        try:
            result = self._handler(action, data)
        except Exception as exc:
            result = {"error": str(exc)}
        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id,
            ),
            body=json.dumps(result),
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
