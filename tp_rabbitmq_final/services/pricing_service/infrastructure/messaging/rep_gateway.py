import zmq


class GatewayResponder:
    def __init__(self, handler_func, bind_addr: str = "tcp://*:5555"):
        self._handler = handler_func
        self._addr = bind_addr

    def start_listening(self):
        ctx = zmq.Context()
        socket = ctx.socket(zmq.REP)
        socket.bind(self._addr)
        print(f"[PricingService] REP en ecoute sur {self._addr}")
        while True:
            message = socket.recv_json()
            action = message.get("action")
            data = message.get("data", {})
            try:
                result = self._handler(action, data)
            except Exception as exc:
                result = {"error": str(exc)}
            socket.send_json(result)
