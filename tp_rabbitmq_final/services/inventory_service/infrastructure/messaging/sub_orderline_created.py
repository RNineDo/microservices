import zmq
import json
import os


class OrderLineCreatedListener:
    def __init__(self, on_orderline_created, connect_addr: str = None):
        self._callback = on_orderline_created
        self._addr = connect_addr or os.getenv("ORDER_PUB_ADDR", "tcp://order_service:5556")

    def start_listening(self):
        ctx = zmq.Context()
        socket = ctx.socket(zmq.SUB)
        socket.connect(self._addr)
        socket.setsockopt_string(zmq.SUBSCRIBE, "orderline.created")
        print(f"[InventoryService] SUB orderline.created sur {self._addr}")
        while True:
            msg = socket.recv_string()
            topic, raw_data = msg.split(" ", 1)
            data = json.loads(raw_data)
            print(f"[InventoryService] Evenement orderline.created recu: {data}")
            self._callback(data)
