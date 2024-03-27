from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, UUID, String, Column, ForeignKey, Date, Float, Boolean, TIMESTAMP, text


class Proband(Base):
    __tablename__ = "PROBAND"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    gender_id = mapped_column(BigInteger, ForeignKey("GENDER.id", ondelete="SET NULL"), nullable=False)
    birthday = mapped_column(Date, nullable=False)
    weight = mapped_column(Float, nullable=False)
    height = mapped_column(Float, nullable=False)
    health = mapped_column(Float, nullable=False)
    country_id = mapped_column(BigInteger, ForeignKey("COUNTRY.id", ondelete="SET NULL"), nullable=False)
    is_active = mapped_column(Boolean, nullable=False)
    last_changed = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # calculate body mass index
    @hybrid_property
    def bmi(self):
        return self.weight / ((self.height/100) ** 2)