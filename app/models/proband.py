from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, UUID, String, Column, ForeignKey

from app.db.session import get_db

with get_db() as db:
    db.query(Proband).all()


class Proband(Base):
    __tablename__ = "PROBAND"

    id = mapped_column(UUID, primary_key=True, autoincrement=True)
    geschlecht = mapped_column(UUID, ForeignKey("GESCHLECHT.id", ondelete="SET NULL"), nullable=False)