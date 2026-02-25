from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    status = Column(String(50), nullable=False, default="pending")


class OrderLineModel(Base):
    __tablename__ = "order_lines"

    id = Column(String, primary_key=True)
    order_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    warehouse_id = Column(String, nullable=True)


def build_tables(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
