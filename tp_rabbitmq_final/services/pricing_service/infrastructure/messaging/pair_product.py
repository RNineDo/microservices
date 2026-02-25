import zmq


class ProductPairServer:
    def __init__(self, handler_func, bind_addr: str = "tcp://*:5557"):
        self._handler = handler_func
        self._addr = bind_addr

    def start_listening(self):
        ctx = zmq.Context()
        socket = ctx.socket(zmq.PAIR)
        socket.bind(self._addr)
        print(f"[PricingService] PAIR en ecoute sur {self._addr}")
        while True:
            message = socket.recv_json()
            try:
                result = self._handler(message)
            except Exception as exc:
                result = {"error": str(exc)}
            socket.send_json(result)
