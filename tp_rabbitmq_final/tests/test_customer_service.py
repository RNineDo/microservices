import pytest
from unittest.mock import MagicMock
from services.customer_service.domain.entities import ClientProfile
from services.customer_service.application.dtos import NewClientInput, ModifyClientInput, ClientOutput


class TestCustomerEntities:
    def test_client_profile_creation(self):
        client = ClientProfile(
            first_name="Marie",
            last_name="Curie",
            email="marie.curie@mail.fr",
        )
        assert client.first_name == "Marie"
        assert client.last_name == "Curie"
        assert client.phone is None
        assert client.id is None

    def test_client_profile_with_phone(self):
        client = ClientProfile(
            first_name="Pierre",
            last_name="Curie",
            email="pierre@mail.fr",
            phone="0601020304",
        )
        assert client.phone == "0601020304"


class TestCustomerDTOs:
    def test_new_client_input(self):
        dto = NewClientInput(
            first_name="Alice",
            last_name="Martin",
            email="alice@test.com",
        )
        assert dto.first_name == "Alice"
        assert dto.phone is None

    def test_modify_client_partial(self):
        dto = ModifyClientInput(email="nouveau@mail.com")
        dumped = dto.model_dump(exclude_none=True)
        assert dumped == {"email": "nouveau@mail.com"}
        assert "first_name" not in dumped

    def test_client_output(self):
        output = ClientOutput(
            id="xyz-789",
            first_name="Bob",
            last_name="Dupont",
            email="bob@test.com",
        )
        assert output.id == "xyz-789"


class TestCustomerRepository:
    def _make_store(self):
        from services.customer_service.infrastructure.db.repository import ClientDataAccess
        mock_uow = MagicMock()
        mock_session = MagicMock()
        mock_uow.begin.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_uow.begin.return_value.__exit__ = MagicMock(return_value=False)
        return ClientDataAccess(mock_uow), mock_session

    def test_insert_calls_session(self):
        store, session = self._make_store()
        store.insert({
            "first_name": "Test",
            "last_name": "User",
            "email": "test@test.com",
        })
        session.add.assert_called_once()

    def test_find_not_found(self):
        store, session = self._make_store()
        session.query.return_value.filter_by.return_value.first.return_value = None
        result = store.find_by_id("inexistant")
        assert result is None
