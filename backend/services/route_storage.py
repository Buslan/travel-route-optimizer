from typing import Dict, Any

from sqlalchemy.orm import Session

from backend.models import SavedRoute, SavedRoutePoint


def save_optimized_route(db: Session, optimization_result: Dict[str, Any]) -> int | None:
    """
    Сохраняет лучший найденный маршрут в базу данных.

    В saved_routes записываются общие характеристики маршрута:
    - начало;
    - конец;
    - расстояние;
    - время;
    - стоимость;
    - итоговая оценка Score.

    В saved_route_points записываются точки маршрута
    в правильном порядке прохождения.
    """

    if optimization_result.get("status") != "success":
        return None

    best_route = optimization_result["best_route"]
    route_points = best_route["route"]
    metrics = best_route["metrics"]
    calculation = best_route["calculation"]

    # Используем ASCII-стрелку, чтобы не было проблем с кодировкой в SQLite/браузере.
    route_name = " -> ".join(route_points)

    saved_route = SavedRoute(
        route_name=route_name,
        start_place=route_points[0],
        finish_place=route_points[-1],
        total_distance=metrics["distance"],
        total_time=metrics["total_time"],
        total_cost=metrics["total_cost"],
        score=calculation["score"]
    )

    db.add(saved_route)
    db.commit()
    db.refresh(saved_route)

    for index, place_code in enumerate(route_points):
        route_point = SavedRoutePoint(
            route_id=saved_route.id,
            place_code=place_code,
            order_index=index
        )

        db.add(route_point)

    db.commit()

    return saved_route.id