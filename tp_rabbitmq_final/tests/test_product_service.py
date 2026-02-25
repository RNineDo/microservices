import pytest
from unittest.mock import MagicMock, patch
from services.product_service.domain.entities import ProductItem, ProductCategory
from services.product_service.application.dtos import NewProductInput, ModifyProductInput, ProductOutput


class TestProductEntities:
    def test_product_item_creation(self):
        item = ProductItem(name="Ecran 27 pouces", category=ProductCategory.ELECTRONICS)
        assert item.name == "Ecran 27 pouces"
        assert item.category == ProductCategory.ELECTRONICS
        assert item.id is None

    def test_product_item_default_category(self):
        item = ProductItem(name="Objet divers")
        assert item.category == ProductCategory.OTHER

    def test_product_category_values(self):
        assert ProductCategory.ELECTRONICS == "electronics"
        assert ProductCategory.CLOTHING == "clothing"
        assert ProductCategory.FOOD == "food"
        assert ProductCategory.BOOKS == "books"


class TestProductDTOs:
    def test_new_product_input_minimal(self):
        dto = NewProductInput(name="Souris sans fil")
        assert dto.name == "Souris sans fil"
        assert dto.category == "other"
        assert dto.description is None

    def test_new_product_input_full(self):
        dto = NewProductInput(
            name="Casque audio",
            description="Bluetooth 5.0",
            category="electronics",
        )
        assert dto.description == "Bluetooth 5.0"
        assert dto.category == "electronics"

    def test_modify_product_input_partial(self):
        dto = ModifyProductInput(name="Nouveau nom")
        dumped = dto.model_dump(exclude_none=True)
        assert dumped == {"name": "Nouveau nom"}

    def test_product_output_with_pricing(self):
        output = ProductOutput(
            id="abc-123",
            name="Clavier",
            category="electronics",
            amount=49.99,
            currency="EUR",
            stock=10,
        )
        assert output.amount == 49.99
        assert output.currency == "EUR"
        assert output.stock == 10


class TestProductRepository:
    def _make_store(self):
        from services.product_service.infrastructure.db.repository import ProductStore
        mock_uow = MagicMock()
        mock_session = MagicMock()
        mock_uow.begin.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_uow.begin.return_value.__exit__ = MagicMock(return_value=False)
        return ProductStore(mock_uow), mock_session

    def test_insert_generates_id(self):
        store, session = self._make_store()
        result = store.insert({"name": "Test", "category": "other"})
        session.add.assert_called_once()
        session.flush.assert_called_once()

    def test_find_by_id_not_found(self):
        store, session = self._make_store()
        session.query.return_value.filter_by.return_value.first.return_value = None
        result = store.find_by_id("inexistant")
        assert result is None
