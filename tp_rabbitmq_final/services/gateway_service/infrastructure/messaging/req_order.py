import zmq
import os


class OrderRequester:
    def __init__(self):
        self._addr = os.getenv("ORDER_REP_ADDR", "tcp://order_service:5555")
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.REQ)
        self._socket.connect(self._addr)

    def send(self, action: str, data: dict = None) -> dict:
        message = {"action": action, "data": data or {}}
        self._socket.send_json(message)
        return self._socket.recv_json()
