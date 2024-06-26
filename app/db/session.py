from sqlalchemy import create_engine,  inspect, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from typing import Generator
from contextlib import contextmanager

# MySQL Settings
MYSQL_HOST = "db"
MYSQL_USER = "root"
MYSQL_PASSWORD = "change-me"
MYSQL_DB = "dbproject"
MYSQL_PORT = "3306"
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

if not database_exists(SQLALCHEMY_DATABASE_URI): create_database(SQLALCHEMY_DATABASE_URI)
# create a new engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    # echo=True
)

# print("all tables")
# Base.metadata.create_all(engine)
#
# # Erstellen eines Inspectors
# inspector = inspect(engine)
#
# # Abrufen der Namen aller Tabellen
# available_tables = inspector.get_table_names()
# print(available_tables)

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
