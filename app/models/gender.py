from main import db
from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, UUID, String, Column, ForeignKey, Date, Float, Boolean


class Gender(Base):
    __tablename__ = "GENDER"

    id = mapped_column(UUID, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
