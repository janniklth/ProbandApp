from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, UUID, String, Column, ForeignKey, Date, Float, Boolean


class Proband(Base):
    __tablename__ = "PROBAND"

    id = mapped_column(UUID, primary_key=True, autoincrement=True)
    firstName = mapped_column(String, nullable=False)
    lastName = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    gender = mapped_column(UUID, ForeignKey("GENDER.id", ondelete="SET NULL"), nullable=False)
    birthday = mapped_column(Date, nullable=False)
    weight = mapped_column(Float, nullable=False)
    height = mapped_column(Float, nullable=False)
    health = mapped_column(Float, nullable=False)
    countryId = mapped_column(UUID, ForeignKey("COUNTRY.id", ondelete="SET NULL"), nullable=False)
    isActive = mapped_column(Boolean, nullable=False)
    lastChanged = mapped_column(Date, nullable=False)