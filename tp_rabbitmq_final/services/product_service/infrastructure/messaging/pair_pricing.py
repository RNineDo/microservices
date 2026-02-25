import zmq
import os


class PricingPairClient:
    def __init__(self, connect_addr: str = None):
        self._addr = connect_addr or os.getenv("PRICING_PAIR_ADDR", "tcp://pricing_service:5557")
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.PAIR)
        self._socket.connect(self._addr)

    def fetch_price(self, product_id: str) -> dict:
        self._socket.send_json({"action": "get_price", "product_id": product_id})
        try:
            return self._socket.recv_json(flags=zmq.NOBLOCK)
        except zmq.Again:
            import time
            time.sleep(0.5)
            try:
                return self._socket.recv_json(flags=zmq.NOBLOCK)
            except zmq.Again:
                return {}
