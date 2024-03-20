from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from typing import Generator
from contextlib import contextmanager
from db.base_class import Base
from models.proband import Proband
from models.gender import Gender
from models.country import Country

# MySQL Settings
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "change-me"
MYSQL_DB = "dbproject"
MYSQL_PORT = "3306"
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


# create a new engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URI, 
    pool_pre_ping=True, 
    # echo=True
    )
print("creating tables")
Base.metadata.create_all(engine)


# Erstellen eines Inspectors
inspector = inspect(engine)

# Abrufen der Namen aller Tabellen
available_tables = inspector.get_table_names()
print(available_tables)

# create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a new context manager
@contextmanager
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()