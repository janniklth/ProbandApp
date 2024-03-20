from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base


class ProbandSickness(Base):
    __tablename__ = "PROBANDSICKNESS"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    probandId = mapped_column(BigInteger, ForeignKey("PROBAND.id"), primary_key=True)
    sicknessId = mapped_column(BigInteger, ForeignKey("SICKNESS.id"), primary_key=True)
