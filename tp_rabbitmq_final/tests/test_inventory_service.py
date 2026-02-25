import pytest
from unittest.mock import MagicMock
from services.inventory_service.domain.entities import StorageLocation, StockEntry
from services.inventory_service.application.dtos import (
    NewWarehouseInput, WarehouseOutput,
    NewStockInput, ModifyStockInput, StockOutput,
)


class TestInventoryEntities:
    def test_storage_location(self):
        loc = StorageLocation(name="Entrepot Paris")
        assert loc.name == "Entrepot Paris"
        assert loc.address is None

    def test_stock_entry_defaults(self):
        entry = StockEntry(product_id="p-1", warehouse_id="w-1")
        assert entry.quantity == 0

    def test_stock_entry_with_qty(self):
        entry = StockEntry(product_id="p-1", warehouse_id="w-1", quantity=100)
        assert entry.quantity == 100


class TestInventoryDTOs:
    def test_new_warehouse(self):
        dto = NewWarehouseInput(name="Lyon", address="Rue de Lyon")
        assert dto.name == "Lyon"

    def test_new_stock(self):
        dto = NewStockInput(product_id="p-1", warehouse_id="w-1", quantity=20)
        assert dto.quantity == 20

    def test_modify_stock(self):
        dto = ModifyStockInput(quantity=50)
        assert dto.quantity == 50

    def test_stock_output(self):
        output = StockOutput(id="s-1", product_id="p-1", warehouse_id="w-1", quantity=30)
        assert output.quantity == 30


class TestInventoryRepository:
    def _make_stores(self):
        from services.inventory_service.infrastructure.db.repository import WarehouseStore, StockStore
        mock_uow = MagicMock()
        mock_session = MagicMock()
        mock_uow.begin.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_uow.begin.return_value.__exit__ = MagicMock(return_value=False)
        return WarehouseStore(mock_uow), StockStore(mock_uow), mock_session

    def test_warehouse_insert(self):
        wh_store, _, session = self._make_stores()
        wh_store.insert({"name": "Test WH"})
        session.add.assert_called_once()

    def test_stock_find_empty(self):
        _, stock_store, session = self._make_stores()
        session.query.return_value.filter_by.return_value.all.return_value = []
        result = stock_store.find_by_product("inexistant")
        assert result == []
