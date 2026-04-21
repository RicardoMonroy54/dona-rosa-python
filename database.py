from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Equivalente al application.properties de Spring
DATABASE_URL = "sqlite:///./donarosa.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()