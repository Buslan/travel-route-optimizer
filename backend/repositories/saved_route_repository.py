from sqlalchemy.orm import Session

from backend.models import SavedRoute, SavedRoutePoint


class SavedRouteRepository:
    """
    Репозиторий для сохранённых маршрутов.

    Отвечает за:
    - создание записи в saved_routes;
    - сохранение точек маршрута в saved_route_points;
    - получение истории рассчитанных маршрутов.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_route(
        self,
        route_name: str,
        start_place: str,
        finish_place: str,
        total_distance: float,
        total_time: float,
        total_cost: float,
        score: float
    ) -> SavedRoute:
        saved_route = SavedRoute(
            route_name=route_name,
            start_place=start_place,
            finish_place=finish_place,
            total_distance=total_distance,
            total_time=total_time,
            total_cost=total_cost,
            score=score
        )

        self.db.add(saved_route)
        self.db.commit()
        self.db.refresh(saved_route)

        return saved_route

    def add_route_point(
        self,
        route_id: int,
        place_code: str,
        order_index: int
    ) -> SavedRoutePoint:
        route_point = SavedRoutePoint(
            route_id=route_id,
            place_code=place_code,
            order_index=order_index
        )

        self.db.add(route_point)
        self.db.commit()

        return route_point

    def get_all(self) -> list[SavedRoute]:
        return (
            self.db.query(SavedRoute)
            .order_by(SavedRoute.created_at.desc())
            .all()
        )

    def count(self) -> int:
        return self.db.query(SavedRoute).count()