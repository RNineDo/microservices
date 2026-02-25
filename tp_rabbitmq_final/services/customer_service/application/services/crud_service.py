from services.customer_service.infrastructure.db.repository import ClientDataAccess
from services.customer_service.infrastructure.db.unit_of_work import ClientWorkUnit
from services.customer_service.application.dtos import NewClientInput, ModifyClientInput


class ClientManager:
    def __init__(self, db_url: str):
        self._uow = ClientWorkUnit(db_url)
        self._store = ClientDataAccess(self._uow)

    def register(self, data: dict) -> dict:
        dto = NewClientInput(**data)
        return self._store.insert(dto.model_dump())

    def fetch_one(self, client_id: str) -> dict:
        record = self._store.find_by_id(client_id)
        if not record:
            return {"error": "Client introuvable"}
        return record

    def fetch_all(self) -> dict:
        records = self._store.list_all()
        return {"items": records}

    def modify(self, data: dict) -> dict:
        client_id = data.pop("id")
        dto = ModifyClientInput(**data)
        updated = self._store.edit(client_id, dto.model_dump(exclude_none=True))
        if not updated:
            return {"error": "Client introuvable"}
        return updated

    def discard(self, client_id: str) -> dict:
        ok = self._store.remove(client_id)
        if not ok:
            return {"error": "Client introuvable"}
        return {"status": "supprime"}
