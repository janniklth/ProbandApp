
from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base


class ProbandMedication(Base):
    __tablename__ = "PROBANDMEDICATION"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    probandId = mapped_column(BigInteger, ForeignKey("PROBAND.id"), primary_key=True)
    medicationId = mapped_column(BigInteger, ForeignKey("MEDICATION.id"), primary_key=True)
