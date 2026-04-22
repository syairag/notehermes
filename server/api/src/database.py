from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create tables if using SQLite (useful for local dev without Postgres)
def init_db():
    if settings.DATABASE_URL.startswith("sqlite"):
        # Import models so SQLAlchemy knows about them
        from src.models import db_models  # noqa: F401
        Base.metadata.create_all(bind=engine, checkfirst=True)

init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
