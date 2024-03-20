from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, UUID, String, Column, ForeignKey, Date, Float, Boolean, TIMESTAMP


class Sickness(Base):
    __tablename__ = "SICKNESS"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)