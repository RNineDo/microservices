from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WarehouseModel(Base):
    __tablename__ = "warehouses"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)


class InventoryModel(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True)
    product_id = Column(String, nullable=False)
    warehouse_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)


def build_tables(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
