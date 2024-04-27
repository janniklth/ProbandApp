from app.db.base_class import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import  String, BigInteger

class Country(Base):
    __tablename__ = "COUNTRY"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
    countrycode = mapped_column(String, nullable=False)
