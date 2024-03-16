from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from contextlib import contextmanager


# MySQL Settings
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "dhbw-mysql"
MYSQL_DB = "2024_inf_db"
MYSQL_PORT = "3306"
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


# create a new engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URI, 
    pool_pre_ping=True, 
    # echo=True
    )

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