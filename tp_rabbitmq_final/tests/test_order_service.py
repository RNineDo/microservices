import pytest
from unittest.mock import MagicMock
from services.order_service.domain.entities import Purchase, PurchaseLine, PurchaseStatus
from services.order_service.application.dtos import (
    NewOrderInput, NewOrderLineInput, ModifyOrderInput,
    OrderOutput, OrderLineOutput,
)


class TestOrderEntities:
    def test_purchase_status_values(self):
        assert PurchaseStatus.PENDING == "pending"
        assert PurchaseStatus.CONFIRMED == "confirmed"
        assert PurchaseStatus.SHIPPED == "shipped"
        assert PurchaseStatus.DELIVERED == "delivered"
        assert PurchaseStatus.CANCELLED == "cancelled"

    def test_purchase_default_status(self):
        order = Purchase(customer_id="c-1")
        assert order.status == PurchaseStatus.PENDING
        assert order.lines == []

    def test_purchase_line(self):
        line = PurchaseLine(product_id="p-1", quantity=5)
        assert line.quantity == 5
        assert line.warehouse_id is None


class TestOrderDTOs:
    def test_new_order_with_lines(self):
        dto = NewOrderInput(
            customer_id="c-1",
            lines=[
                NewOrderLineInput(product_id="p-1", quantity=2),
                NewOrderLineInput(product_id="p-2", quantity=1, warehouse_id="w-1"),
            ],
        )
        assert len(dto.lines) == 2
        assert dto.lines[0].quantity == 2
        assert dto.lines[1].warehouse_id == "w-1"

    def test_new_order_empty_lines(self):
        dto = NewOrderInput(customer_id="c-1")
        assert dto.lines == []

    def test_modify_order(self):
        dto = ModifyOrderInput(status="confirmed")
        assert dto.status == "confirmed"

    def test_order_output(self):
        output = OrderOutput(id="o-1", customer_id="c-1", status="pending")
        assert output.lines == []

    def test_orderline_output(self):
        output = OrderLineOutput(
            id="ol-1", order_id="o-1", product_id="p-1", quantity=3
        )
        assert output.quantity == 3


class TestOrderRepository:
    def _make_stores(self):
        from services.order_service.infrastructure.db.repository import PurchaseStore, PurchaseLineStore
        mock_uow = MagicMock()
        mock_session = MagicMock()
        mock_uow.begin.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_uow.begin.return_value.__exit__ = MagicMock(return_value=False)
        return PurchaseStore(mock_uow), PurchaseLineStore(mock_uow), mock_session

    def test_order_insert(self):
        order_store, _, session = self._make_stores()
        order_store.insert({"customer_id": "c-1", "status": "pending"})
        session.add.assert_called_once()

    def test_order_not_found(self):
        order_store, _, session = self._make_stores()
        session.query.return_value.filter_by.return_value.first.return_value = None
        result = order_store.find_by_id("inexistant")
        assert result is None

    def test_orderline_find_empty(self):
        _, line_store, session = self._make_stores()
        session.query.return_value.filter_by.return_value.all.return_value = []
        result = line_store.find_by_order("inexistant")
        assert result == []
