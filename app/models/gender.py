from app.db.base_class import Base
from sqlalchemy.orm import  mapped_column
from sqlalchemy import String, BigInteger


class Gender(Base):
    __tablename__ = "GENDER"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
