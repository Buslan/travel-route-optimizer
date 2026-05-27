from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./travel_routes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """
    Создаёт подключение к базе данных для FastAPI endpoint-ов.
    После выполнения запроса подключение закрывается.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Создаёт таблицы базы данных, если они ещё не существуют.
    """

    Base.metadata.create_all(bind=engine)