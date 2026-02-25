import zmq
import json
from services.order_service.domain.events import ORDER_CREATED, ORDERLINE_CREATED


class OrderEventEmitter:
    def __init__(self, bind_addr: str = "tcp://*:5556"):
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.PUB)
        self._socket.bind(bind_addr)

    def emit_order_created(self, order_data: dict):
        payload = f"{ORDER_CREATED} {json.dumps(order_data)}"
        self._socket.send_string(payload)

    def emit_orderline_created(self, line_data: dict):
        payload = f"{ORDERLINE_CREATED} {json.dumps(line_data)}"
        self._socket.send_string(payload)
