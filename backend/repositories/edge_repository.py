from sqlalchemy.orm import Session

from backend.models import Edge


class EdgeRepository:
    """
    Репозиторий для работы с таблицей edges.

    Таблица edges хранит рёбра графа:
    - расстояние между городами;
    - время перемещения;
    - стоимость перемещения;
    - тип транспорта.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Edge]:
        return self.db.query(Edge).all()

    def count(self) -> int:
        return self.db.query(Edge).count()