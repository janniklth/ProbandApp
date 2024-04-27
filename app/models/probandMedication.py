from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column
from app.db.base_class import Base


class ProbandMedication(Base):
    __tablename__ = "PROBANDMEDICATION"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    proband_id = mapped_column(BigInteger, ForeignKey("PROBAND.id"), primary_key=True)
    medication_id = mapped_column(BigInteger, ForeignKey("MEDICATION.id"), primary_key=True)
