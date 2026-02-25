import zmq
import json
import os


class ProductCreatedListener:
    def __init__(self, on_product_created, connect_addr: str = None):
        self._callback = on_product_created
        self._addr = connect_addr or os.getenv("PRODUCT_PUB_ADDR", "tcp://product_service:5556")

    def start_listening(self):
        ctx = zmq.Context()
        socket = ctx.socket(zmq.SUB)
        socket.connect(self._addr)
        socket.setsockopt_string(zmq.SUBSCRIBE, "product.created")
        print(f"[PricingService] SUB product.created sur {self._addr}")
        while True:
            msg = socket.recv_string()
            topic, raw_data = msg.split(" ", 1)
            data = json.loads(raw_data)
            print(f"[PricingService] Evenement product.created recu: {data}")
            self._callback(data)
