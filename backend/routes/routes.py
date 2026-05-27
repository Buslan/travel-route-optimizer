from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.repositories.saved_route_repository import SavedRouteRepository


router = APIRouter(
    prefix="/db",
    tags=["Saved routes"]
)


@router.get("/saved-routes")
def get_saved_routes(db: Session = Depends(get_db)):
    """
    Возвращает историю сохранённых маршрутов.

    Endpoint не обращается к SQLAlchemy напрямую.
    Для работы с таблицами saved_routes и saved_route_points
    используется SavedRouteRepository.
    """

    repository = SavedRouteRepository(db)
    saved_routes = repository.get_all()

    return {
        "count": len(saved_routes),
        "routes": [
            {
                "id": route.id,
                "route_name": route.route_name,
                "start_place": route.start_place,
                "finish_place": route.finish_place,
                "total_distance": route.total_distance,
                "total_time": route.total_time,
                "total_cost": route.total_cost,
                "score": route.score,
                "created_at": route.created_at,
                "points": [
                    {
                        "place_code": point.place_code,
                        "order_index": point.order_index
                    }
                    for point in sorted(route.points, key=lambda item: item.order_index)
                ]
            }
            for route in saved_routes
        ]
    }