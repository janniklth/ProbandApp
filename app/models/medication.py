from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, UUID, String, Column, ForeignKey, Date, Float, Boolean

class Medication(Base):
    __tablename__ = "MEDICATION"

    id = mapped_column(UUID, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)