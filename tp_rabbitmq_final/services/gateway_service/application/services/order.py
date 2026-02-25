from services.gateway_service.infrastructure.messaging.req_order import OrderRequester


class OrderProxy:
    def __init__(self):
        self._requester = OrderRequester()

    def register(self, payload: dict) -> dict:
        return self._requester.send("create", payload)

    def fetch_one(self, pk: str) -> dict:
        return self._requester.send("get", {"id": pk})

    def modify(self, pk: str, payload: dict) -> dict:
        payload["id"] = pk
        return self._requester.send("update_status", payload)
