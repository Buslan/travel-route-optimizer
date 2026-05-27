from sqlalchemy.orm import Session

from backend.models import Place


class PlaceRepository:
    """
    Репозиторий для работы с таблицей places.

    Этот слой изолирует SQLAlchemy-запросы от routes и services.
    Благодаря этому endpoint-ы не обращаются к базе напрямую.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Place]:
        return self.db.query(Place).all()

    def get_by_code(self, code: str) -> Place | None:
        return self.db.query(Place).filter(Place.code == code).first()

    def count(self) -> int:
        return self.db.query(Place).count()