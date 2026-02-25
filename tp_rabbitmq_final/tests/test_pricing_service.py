import pytest
from unittest.mock import MagicMock
from services.pricing_service.domain.entities import PriceRecord
from services.pricing_service.application.dtos import NewPricingInput, ModifyPricingInput, PricingOutput


class TestPricingEntities:
    def test_price_record_defaults(self):
        record = PriceRecord(product_id="prod-001")
        assert record.amount == 0.0
        assert record.currency == "EUR"
        assert record.id is None

    def test_price_record_custom(self):
        record = PriceRecord(product_id="prod-002", amount=29.99, currency="USD")
        assert record.amount == 29.99
        assert record.currency == "USD"


class TestPricingDTOs:
    def test_new_pricing_input_defaults(self):
        dto = NewPricingInput(product_id="prod-001")
        assert dto.amount == 0.0
        assert dto.currency == "EUR"

    def test_new_pricing_input_custom(self):
        dto = NewPricingInput(product_id="prod-001", amount=15.50, currency="GBP")
        assert dto.amount == 15.50
        assert dto.currency == "GBP"

    def test_modify_pricing_partial(self):
        dto = ModifyPricingInput(amount=42.0)
        dumped = dto.model_dump(exclude_none=True)
        assert dumped == {"amount": 42.0}
        assert "currency" not in dumped

    def test_pricing_output(self):
        output = PricingOutput(id="p-1", product_id="prod-1", amount=99.99, currency="EUR")
        assert output.amount == 99.99


class TestPricingRepository:
    def _make_store(self):
        from services.pricing_service.infrastructure.db.repository import PriceStore
        mock_uow = MagicMock()
        mock_session = MagicMock()
        mock_uow.begin.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_uow.begin.return_value.__exit__ = MagicMock(return_value=False)
        return PriceStore(mock_uow), mock_session

    def test_insert_calls_session(self):
        store, session = self._make_store()
        store.insert({"product_id": "p-1", "amount": 10.0, "currency": "EUR"})
        session.add.assert_called_once()

    def test_find_not_found(self):
        store, session = self._make_store()
        session.query.return_value.filter_by.return_value.first.return_value = None
        result = store.find_by_product_id("inexistant")
        assert result is None
