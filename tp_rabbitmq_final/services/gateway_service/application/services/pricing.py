from services.gateway_service.infrastructure.messaging.req_pricing import PricingRequester


class PricingProxy:
    def __init__(self):
        self._requester = PricingRequester()

    def register(self, payload: dict) -> dict:
        return self._requester.send("create", payload)

    def fetch_by_product(self, product_pk: str) -> dict:
        return self._requester.send("get_by_product", {"product_id": product_pk})

    def modify_by_product(self, product_pk: str, payload: dict) -> dict:
        payload["product_id"] = product_pk
        return self._requester.send("update_by_product", payload)

    def discard(self, pk: str) -> dict:
        return self._requester.send("delete", {"id": pk})
