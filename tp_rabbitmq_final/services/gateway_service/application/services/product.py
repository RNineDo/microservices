from services.gateway_service.infrastructure.messaging.req_product import ProductRequester


class ProductProxy:
    def __init__(self):
        self._requester = ProductRequester()

    def register(self, payload: dict) -> dict:
        return self._requester.send("create", payload)

    def fetch_one(self, pk: str) -> dict:
        return self._requester.send("get", {"id": pk})

    def fetch_all(self) -> dict:
        return self._requester.send("get_all")

    def modify(self, pk: str, payload: dict) -> dict:
        payload["id"] = pk
        return self._requester.send("update", payload)

    def discard(self, pk: str) -> dict:
        return self._requester.send("delete", {"id": pk})
