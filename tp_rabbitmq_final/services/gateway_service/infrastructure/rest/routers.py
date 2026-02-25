from fastapi import APIRouter, HTTPException
from services.gateway_service.application.services.product import ProductProxy
from services.gateway_service.application.services.customer import CustomerProxy
from services.gateway_service.application.services.inventory import InventoryProxy
from services.gateway_service.application.services.pricing import PricingProxy
from services.gateway_service.application.services.order import OrderProxy

api_router = APIRouter(prefix="/api")

product_proxy = ProductProxy()
customer_proxy = CustomerProxy()
inventory_proxy = InventoryProxy()
pricing_proxy = PricingProxy()
order_proxy = OrderProxy()


@api_router.post("/product")
def add_product(payload: dict):
    result = product_proxy.register(payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.get("/product/{pk}")
def fetch_product(pk: str):
    result = product_proxy.fetch_one(pk)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@api_router.put("/product/{pk}")
def modify_product(pk: str, payload: dict):
    result = product_proxy.modify(pk, payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.post("/customer")
def add_customer(payload: dict):
    result = customer_proxy.register(payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.get("/customer/{pk}")
def fetch_customer(pk: str):
    result = customer_proxy.fetch_one(pk)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@api_router.post("/warehouse")
def add_warehouse(payload: dict):
    result = inventory_proxy.register_warehouse(payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.get("/warehouse")
def list_warehouses():
    result = inventory_proxy.fetch_all_warehouses()
    return result


@api_router.post("/inventory")
def add_inventory(payload: dict):
    result = inventory_proxy.register_stock(payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.get("/inventory/{product_pk}")
def fetch_inventory(product_pk: str):
    result = inventory_proxy.fetch_stock_by_product(product_pk)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@api_router.patch("/inventory/{warehouse_pk}/{product_pk}")
def modify_inventory(warehouse_pk: str, product_pk: str, payload: dict):
    result = inventory_proxy.modify_stock(warehouse_pk, product_pk, payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.post("/pricing")
def add_pricing(payload: dict):
    result = pricing_proxy.register(payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.get("/pricing/{product_pk}")
def fetch_pricing(product_pk: str):
    result = pricing_proxy.fetch_by_product(product_pk)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@api_router.post("/order")
def add_order(payload: dict):
    result = order_proxy.register(payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@api_router.get("/order/{pk}")
def fetch_order(pk: str):
    result = order_proxy.fetch_one(pk)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@api_router.patch("/order/{pk}")
def modify_order(pk: str, payload: dict):
    result = order_proxy.modify(pk, payload)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result
