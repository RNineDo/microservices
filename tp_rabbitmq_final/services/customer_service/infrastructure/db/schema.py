from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)


def build_tables(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
