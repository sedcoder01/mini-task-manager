from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from os import getcwd
from app.config import settings
from urllib.parse import quote_plus

DB_URL = URL.create(
    'postgresql+psycopg2',
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    database=settings.DB_NAME
)
# DB_URL = f'postgresql://{settings.DB_USER}:{password}@{settings.DB_HOST}/{settings.DB_NAME}'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()