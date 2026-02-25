import zmq
import json
from services.customer_service.domain.events import CUSTOMER_CREATED


class CustomerEventEmitter:
    def __init__(self, bind_addr: str = "tcp://*:5556"):
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.PUB)
        self._socket.bind(bind_addr)

    def emit_created(self, customer_data: dict):
        payload = f"{CUSTOMER_CREATED} {json.dumps(customer_data)}"
        self._socket.send_string(payload)
