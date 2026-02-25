import zmq
import os


class CustomerRequester:
    def __init__(self):
        self._addr = os.getenv("CUSTOMER_REP_ADDR", "tcp://customer_service:5555")
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.REQ)
        self._socket.connect(self._addr)

    def send(self, action: str, data: dict = None) -> dict:
        message = {"action": action, "data": data or {}}
        self._socket.send_json(message)
        return self._socket.recv_json()
