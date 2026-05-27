from typing import Dict, Any

from sqlalchemy.orm import Session

from backend.repositories.saved_route_repository import SavedRouteRepository


def save_optimized_route(db: Session, optimization_result: Dict[str, Any]) -> int | None:
    """
    Сохраняет лучший найденный маршрут в базу данных.

    Слой service не работает с SQLAlchemy напрямую.
    Для сохранения используется SavedRouteRepository.
    """

    if optimization_result.get("status") != "success":
        return None

    best_route = optimization_result["best_route"]
    route_points = best_route["route"]
    metrics = best_route["metrics"]
    calculation = best_route["calculation"]

    route_name = " -> ".join(route_points)

    repository = SavedRouteRepository(db)

    saved_route = repository.create_route(
        route_name=route_name,
        start_place=route_points[0],
        finish_place=route_points[-1],
        total_distance=metrics["distance"],
        total_time=metrics["total_time"],
        total_cost=metrics["total_cost"],
        score=calculation["score"]
    )

    for index, place_code in enumerate(route_points):
        repository.add_route_point(
            route_id=saved_route.id,
            place_code=place_code,
            order_index=index
        )

    return saved_route.id