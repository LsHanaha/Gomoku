from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

_db_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}" \
          f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
engine = create_engine(_db_url)


def get_product_settings():
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal


Base = declarative_base()


def get_db():
    SessionLocal = get_product_settings()
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.close()


# alembic revision --autogenerate -m "message" --head head
# alembic upgrade head
