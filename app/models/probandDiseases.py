from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base


class ProbandDiseases(Base):
    __tablename__ = "PROBANDDISEASES"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    probandId = mapped_column(BigInteger, ForeignKey("PROBAND.id"), primary_key=True)
    sicknessId = mapped_column(BigInteger, ForeignKey("DISEASES.id"), primary_key=True)
