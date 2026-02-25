from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PricingModel(Base):
    __tablename__ = "pricing"

    id = Column(String, primary_key=True)
    product_id = Column(String, nullable=False, unique=True)
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), nullable=False, default="EUR")


def build_tables(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
