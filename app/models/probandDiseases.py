from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column
from app.db.base_class import Base


class ProbandDiseases(Base):
    __tablename__ = "PROBANDDISEASES"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    proband_id = mapped_column(BigInteger, ForeignKey("PROBAND.id"), primary_key=True)
    sickness_id = mapped_column(BigInteger, ForeignKey("DISEASES.id"), primary_key=True)
