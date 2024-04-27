from app.db.base_class import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger, String


class Diseases(Base):
    __tablename__ = "DISEASES"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)