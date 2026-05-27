from itertools import permutations
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

from backend.models import Place, Edge


def load_graph_from_db(db: Session) -> Dict[str, Any]:
    """
    Загружает вершины и рёбра графа из SQLite.

    Вершины графа:
    places

    Рёбра графа:
    edges

    Возвращает структуру:
    {
        "places": {...},
        "edges": {...}
    }
    """

    places_from_db = db.query(Place).all()
    edges_from_db = db.query(Edge).all()

    places = {}

    for place in places_from_db:
        places[place.code] = {
            "id": place.id,
            "code": place.code,
            "name_ru": place.name_ru,
            "name_en": place.name_en,
            "country": place.country,
            "rating": place.rating,
            "visit_cost": place.visit_cost,
            "visit_time": place.visit_time,
            "categories": place.categories.split(","),
            "latitude": place.latitude,
            "longitude": place.longitude
        }

    edges = {}

    for edge in edges_from_db:
        from_code = edge.from_place.code
        to_code = edge.to_place.code

        edges[(from_code, to_code)] = {
            "distance": edge.distance,
            "time": edge.travel_time,
            "cost": edge.travel_cost,
            "transport_type": edge.transport_type
        }

    return {
        "places": places,
        "edges": edges
    }


def validate_route_points(
    places: Dict[str, Dict[str, Any]],
    start: str,
    finish: str,
    stops: List[str]
) -> Optional[str]:
    """
    Проверяет, существуют ли выбранные пользователем точки в базе.
    """

    all_points = [start, finish] + stops

    for point in all_points:
        if point not in places:
            return f"Точка '{point}' отсутствует в базе данных."

    return None


def get_edge_data(
    edges: Dict[tuple, Dict[str, float]],
    from_place: str,
    to_place: str
) -> Dict[str, float]:
    """
    Возвращает данные ребра между двумя точками.

    Для учебного проекта граф считается неориентированным:
    Amsterdam -> Utrecht и Utrecht -> Amsterdam имеют одинаковые веса.
    """

    if (from_place, to_place) in edges:
        return edges[(from_place, to_place)]

    if (to_place, from_place) in edges:
        return edges[(to_place, from_place)]

    return {
        "distance": 999,
        "time": 999,
        "cost": 999,
        "transport_type": "unknown"
    }


def calculate_route_metrics(
    route: List[str],
    places: Dict[str, Dict[str, Any]],
    edges: Dict[tuple, Dict[str, float]]
) -> Dict[str, Any]:
    """
    Считает основные характеристики маршрута:
    - суммарное расстояние;
    - суммарное время;
    - суммарную стоимость;
    - средний рейтинг посещаемых мест.
    """

    total_distance = 0
    total_travel_time = 0
    total_travel_cost = 0
    total_visit_time = 0
    total_visit_cost = 0
    total_rating = 0

    for place_code in route:
        place_data = places[place_code]

        total_visit_time += place_data["visit_time"]
        total_visit_cost += place_data["visit_cost"]
        total_rating += place_data["rating"]

    for i in range(len(route) - 1):
        edge = get_edge_data(edges, route[i], route[i + 1])

        total_distance += edge["distance"]
        total_travel_time += edge["time"]
        total_travel_cost += edge["cost"]

    total_time = total_travel_time + total_visit_time
    total_cost = total_travel_cost + total_visit_cost
    average_rating = total_rating / len(route)

    return {
        "distance": round(total_distance, 2),
        "travel_time": round(total_travel_time, 2),
        "visit_time": round(total_visit_time, 2),
        "total_time": round(total_time, 2),
        "travel_cost": round(total_travel_cost, 2),
        "visit_cost": round(total_visit_cost, 2),
        "total_cost": round(total_cost, 2),
        "average_rating": round(average_rating, 2)
    }


def calculate_preference_score(
    route: List[str],
    preferences: List[str],
    places: Dict[str, Dict[str, Any]]
) -> float:
    """
    Считает совпадение маршрута с интересами пользователя.
    """

    if not preferences:
        return 0.5

    matches = 0
    total_possible_matches = len(route) * len(preferences)

    for place_code in route:
        place_categories = places[place_code]["categories"]

        for preference in preferences:
            if preference in place_categories:
                matches += 1

    return round(matches / total_possible_matches, 3)


def get_weights(priority: str) -> Dict[str, float]:
    """
    Возвращает веса критериев в зависимости от выбранного приоритета.

    Score(R) =
    w_time * (1 - T_norm) +
    w_cost * (1 - C_norm) +
    w_preferences * P_norm +
    w_rating * Q_norm
    """

    weights = {
        "balanced": {
            "time": 0.30,
            "cost": 0.25,
            "preferences": 0.25,
            "rating": 0.20
        },
        "fast": {
            "time": 0.50,
            "cost": 0.15,
            "preferences": 0.20,
            "rating": 0.15
        },
        "cheap": {
            "time": 0.15,
            "cost": 0.50,
            "preferences": 0.20,
            "rating": 0.15
        },
        "preferences": {
            "time": 0.15,
            "cost": 0.15,
            "preferences": 0.50,
            "rating": 0.20
        }
    }

    return weights.get(priority, weights["balanced"])


def normalize(value: float, min_value: float, max_value: float) -> float:
    """
    Нормализация значения в диапазон от 0 до 1.
    Если все значения одинаковые, возвращается 0.5.
    """

    if max_value == min_value:
        return 0.5

    return (value - min_value) / (max_value - min_value)


def optimize_route_from_db(
    db: Session,
    start: str,
    finish: str,
    stops: List[str],
    budget: float,
    max_time: float,
    preferences: List[str],
    priority: str
) -> Dict[str, Any]:
    """
    Главная функция оптимизации маршрута на основе данных из SQLite.

    Вход:
    start — начальная точка
    finish — конечная точка
    stops — промежуточные точки
    budget — максимальный бюджет
    max_time — максимальное время
    preferences — интересы пользователя
    priority — приоритет оптимизации

    Алгоритм:
    1. Загружаем вершины и рёбра графа из базы данных.
    2. Генерируем все перестановки промежуточных точек.
    3. Для каждого маршрута считаем стоимость, время, рейтинг, предпочтения.
    4. Отбрасываем маршруты, которые не проходят ограничения.
    5. Нормализуем показатели.
    6. Считаем итоговую оценку Score.
    7. Выбираем маршрут с максимальным Score.
    """

    graph = load_graph_from_db(db)
    places = graph["places"]
    edges = graph["edges"]

    validation_error = validate_route_points(
        places=places,
        start=start,
        finish=finish,
        stops=stops
    )

    if validation_error:
        return {
            "status": "validation_error",
            "message": validation_error
        }

    candidate_routes = []

    if stops:
        stop_orders = permutations(stops)
    else:
        stop_orders = [tuple()]

    for stop_order in stop_orders:
        route = [start] + list(stop_order) + [finish]

        metrics = calculate_route_metrics(
            route=route,
            places=places,
            edges=edges
        )

        preference_score = calculate_preference_score(
            route=route,
            preferences=preferences,
            places=places
        )

        candidate_routes.append({
            "route": route,
            "metrics": metrics,
            "preference_score": preference_score
        })

    feasible_routes = []

    for item in candidate_routes:
        total_cost = item["metrics"]["total_cost"]
        total_time = item["metrics"]["total_time"]

        if total_cost <= budget and total_time <= max_time:
            feasible_routes.append(item)

    if not feasible_routes:
        return {
            "status": "no_solution",
            "message": "Не найден маршрут, который укладывается в заданный бюджет и время.",
            "all_routes": candidate_routes,
            "data_source": "SQLite database"
        }

    min_time = min(item["metrics"]["total_time"] for item in feasible_routes)
    max_route_time = max(item["metrics"]["total_time"] for item in feasible_routes)

    min_cost = min(item["metrics"]["total_cost"] for item in feasible_routes)
    max_cost = max(item["metrics"]["total_cost"] for item in feasible_routes)

    min_rating = min(item["metrics"]["average_rating"] for item in feasible_routes)
    max_rating = max(item["metrics"]["average_rating"] for item in feasible_routes)

    weights = get_weights(priority)

    for item in feasible_routes:
        metrics = item["metrics"]

        time_norm = normalize(metrics["total_time"], min_time, max_route_time)
        cost_norm = normalize(metrics["total_cost"], min_cost, max_cost)
        rating_norm = normalize(metrics["average_rating"], min_rating, max_rating)
        preference_norm = item["preference_score"]

        score = (
            weights["time"] * (1 - time_norm) +
            weights["cost"] * (1 - cost_norm) +
            weights["preferences"] * preference_norm +
            weights["rating"] * rating_norm
        )

        item["calculation"] = {
            "time_norm": round(time_norm, 3),
            "cost_norm": round(cost_norm, 3),
            "preference_norm": round(preference_norm, 3),
            "rating_norm": round(rating_norm, 3),
            "weights": weights,
            "score_formula": (
                "Score = w_time*(1-T_norm) + "
                "w_cost*(1-C_norm) + "
                "w_preferences*P_norm + "
                "w_rating*Q_norm"
            ),
            "score": round(score, 3),
            "score_percent": round(score * 100, 1)
        }

    feasible_routes.sort(
        key=lambda item: item["calculation"]["score"],
        reverse=True
    )

    best_route = feasible_routes[0]

    return {
        "status": "success",
        "data_source": "SQLite database",
        "best_route": best_route,
        "alternative_routes": feasible_routes[1:],
        "all_feasible_routes": feasible_routes,
        "math_model": {
            "graph": "G = (V, E)",
            "objective_function": (
                "Score(R) = w1*(1-T_norm) + "
                "w2*(1-C_norm) + "
                "w3*P_norm + "
                "w4*Q_norm"
            ),
            "constraints": [
                "T(R) <= T_max",
                "C(R) <= B"
            ],
            "description": (
                "Маршрут рассматривается как путь в неориентированном "
                "взвешенном графе. Вершины графа — города, рёбра — возможные "
                "переезды между ними. Данные о вершинах и рёбрах загружаются "
                "из SQLite-базы данных."
            )
        }
    }