from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, UUID, String, Column, ForeignKey, Date, Float, Boolean, TIMESTAMP


class Proband(Base):
    __tablename__ = "PROBAND"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    firstName = mapped_column(String, nullable=False)
    lastName = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    gender = mapped_column(BigInteger, ForeignKey("GENDER.id", ondelete="SET NULL"), nullable=False)
    birthday = mapped_column(Date, nullable=False)
    weight = mapped_column(Float, nullable=False)
    height = mapped_column(Float, nullable=False)
    health = mapped_column(Float, nullable=False)
    countryId = mapped_column(BigInteger, ForeignKey("COUNTRY.id", ondelete="SET NULL"), nullable=False)
    isActive = mapped_column(Boolean, nullable=False)
    lastChanged = mapped_column(TIMESTAMP, nullable=False)