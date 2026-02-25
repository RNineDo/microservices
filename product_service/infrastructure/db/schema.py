from sqlalchemy import Column, String, Text, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, default="other")


def build_tables(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
