import pika
import json
import time


class ProductCreatedListener:
    def __init__(self, on_product_created, rabbitmq_host: str = "rabbitmq"):
        self._callback = on_product_created
        self._host = rabbitmq_host

    def start_listening(self):
        for _ in range(15):
            try:
                conn = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self._host)
                )
                channel = conn.channel()
                channel.exchange_declare(exchange="events", exchange_type="topic")
                result = channel.queue_declare(queue="pricing_product_created", durable=True)
                queue_name = result.method.queue
                channel.queue_bind(
                    exchange="events",
                    queue=queue_name,
                    routing_key="product.created",
                )
                channel.basic_consume(
                    queue=queue_name,
                    on_message_callback=self._handle_event,
                    auto_ack=True,
                )
                print("[PricingService] Abonne a product.created")
                channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                print("[PricingService] Attente RabbitMQ pour SUB product.created...")
                time.sleep(3)

    def _handle_event(self, ch, method, props, body):
        data = json.loads(body)
        print(f"[PricingService] Evenement product.created recu: {data}")
        self._callback(data)
