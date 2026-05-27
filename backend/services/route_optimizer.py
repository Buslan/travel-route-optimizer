from itertools import permutations
from typing import List, Dict, Any, Optional
from math import factorial

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

    if start == finish:
        return "Начальная и конечная точки не должны совпадать."

    return None


def get_edge_data(
    edges: Dict[tuple, Dict[str, float]],
    from_place: str,
    to_place: str
) -> Dict[str, float]:
    """
    Возвращает данные ребра между двумя точками.

    Для учебного проекта граф считается неориентированным:
    Moscow -> Paris и Paris -> Moscow имеют одинаковые веса.
    """

    if (from_place, to_place) in edges:
        return edges[(from_place, to_place)]

    if (to_place, from_place) in edges:
        return edges[(to_place, from_place)]

    return {
        "distance": 999999,
        "time": 999999,
        "cost": 999999,
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

    P(R) = matches / possible_matches
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


def calculate_diversity_score(
    route: List[str],
    places: Dict[str, Dict[str, Any]]
) -> float:
    """
    Считает разнообразие маршрута по категориям.

    Идея:
    маршрут лучше, если в нём есть разные типы впечатлений:
    культура, история, море, природа, архитектура, еда и т.д.

    D(R) = unique_categories / all_categories
    """

    all_categories = set()
    route_categories = set()

    for place_data in places.values():
        for category in place_data["categories"]:
            all_categories.add(category)

    for place_code in route:
        for category in places[place_code]["categories"]:
            route_categories.add(category)

    if not all_categories:
        return 0.0

    return round(len(route_categories) / len(all_categories), 3)


def calculate_constraint_penalty(
    total_time: float,
    total_cost: float,
    max_time: float,
    budget: float
) -> float:
    """
    Считает мягкий штраф за приближение к ограничениям.

    Даже если маршрут укладывается в ограничения, он может быть
    слишком близко к лимитам. Например, если маршрут использует
    99% бюджета и 99% времени, это менее устойчивый вариант.

    penalty(R) = 0.5 * time_load + 0.5 * cost_load

    где:
    time_load = T(R) / T_max
    cost_load = C(R) / B
    """

    if max_time <= 0 or budget <= 0:
        return 1.0

    time_load = min(total_time / max_time, 1)
    cost_load = min(total_cost / budget, 1)

    penalty = 0.5 * time_load + 0.5 * cost_load

    return round(penalty, 3)


def get_weights(priority: str) -> Dict[str, float]:
    """
    Возвращает веса критериев в зависимости от выбранного приоритета.

    Расширенная модель:

    Score(R) =
    w_time * (1 - T*) +
    w_cost * (1 - C*) +
    w_preferences * P* +
    w_rating * Q* +
    w_diversity * D* -
    lambda_penalty * penalty(R)
    """

    weights = {
        "balanced": {
            "time": 0.25,
            "cost": 0.22,
            "preferences": 0.23,
            "rating": 0.18,
            "diversity": 0.12,
            "penalty": 0.10
        },
        "fast": {
            "time": 0.43,
            "cost": 0.14,
            "preferences": 0.16,
            "rating": 0.14,
            "diversity": 0.13,
            "penalty": 0.10
        },
        "cheap": {
            "time": 0.14,
            "cost": 0.43,
            "preferences": 0.16,
            "rating": 0.14,
            "diversity": 0.13,
            "penalty": 0.10
        },
        "preferences": {
            "time": 0.13,
            "cost": 0.13,
            "preferences": 0.40,
            "rating": 0.17,
            "diversity": 0.17,
            "penalty": 0.10
        }
    }

    return weights.get(priority, weights["balanced"])


def normalize(value: float, min_value: float, max_value: float) -> float:
    """
    Нормализация значения в диапазон от 0 до 1.

    x* = (x - x_min) / (x_max - x_min)

    Если все значения одинаковые, возвращается 0.5.
    """

    if max_value == min_value:
        return 0.5

    return (value - min_value) / (max_value - min_value)


def build_algorithm_info(stops_count: int, generated_routes_count: int) -> Dict[str, Any]:
    """
    Возвращает информацию об алгоритмической сложности.

    Для n промежуточных точек полный перебор имеет сложность O(n!).
    В учебном проекте это допустимо, потому что количество остановок ограничено.
    """

    theoretical_routes = factorial(stops_count) if stops_count > 0 else 1

    return {
        "method": "Полный перебор перестановок промежуточных точек",
        "complexity": "O(n!)",
        "stops_count": stops_count,
        "theoretical_routes_count": theoretical_routes,
        "generated_routes_count": generated_routes_count,
        "explanation": (
            "Для малого количества промежуточных точек полный перебор позволяет "
            "сравнить все возможные порядки посещения и гарантированно выбрать "
            "лучший маршрут среди допустимых вариантов."
        )
    }


def build_calculation_explanation(
    best_route: Dict[str, Any],
    feasible_routes_count: int,
    candidate_routes_count: int
) -> Dict[str, Any]:
    """
    Формирует текстовое объяснение результата для защиты проекта.
    """

    route_text = " -> ".join(best_route["route"])
    score = best_route["calculation"]["score"]
    score_percent = best_route["calculation"]["score_percent"]

    return {
        "selected_route": route_text,
        "reason": (
            f"Маршрут '{route_text}' выбран, потому что он имеет максимальное "
            f"значение целевой функции Score(R) = {score} среди всех допустимых маршрутов."
        ),
        "candidate_routes_count": candidate_routes_count,
        "feasible_routes_count": feasible_routes_count,
        "score_percent": score_percent,
        "interpretation": (
            "Значение Score(R) объединяет время, стоимость, совпадение с интересами, "
            "рейтинг, разнообразие категорий и штраф за приближение к ограничениям. "
            "Чем выше Score(R), тем более предпочтительным считается маршрут."
        )
    }


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

    Алгоритм:
    1. Загружаем вершины и рёбра графа из базы данных.
    2. Генерируем все перестановки промежуточных точек.
    3. Для каждого маршрута считаем стоимость, время, рейтинг, предпочтения.
    4. Дополнительно считаем разнообразие маршрута и штраф за близость к лимитам.
    5. Отбрасываем маршруты, которые не проходят ограничения.
    6. Нормализуем показатели.
    7. Считаем расширенную итоговую оценку Score(R).
    8. Выбираем маршрут с максимальным Score(R).
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

        diversity_score = calculate_diversity_score(
            route=route,
            places=places
        )

        penalty_score = calculate_constraint_penalty(
            total_time=metrics["total_time"],
            total_cost=metrics["total_cost"],
            max_time=max_time,
            budget=budget
        )

        candidate_routes.append({
            "route": route,
            "metrics": metrics,
            "preference_score": preference_score,
            "diversity_score": diversity_score,
            "penalty_score": penalty_score
        })

    feasible_routes = []

    for item in candidate_routes:
        total_cost = item["metrics"]["total_cost"]
        total_time = item["metrics"]["total_time"]

        if total_cost <= budget and total_time <= max_time:
            feasible_routes.append(item)

    algorithm_info = build_algorithm_info(
        stops_count=len(stops),
        generated_routes_count=len(candidate_routes)
    )

    if not feasible_routes:
        return {
            "status": "no_solution",
            "message": "Не найден маршрут, который укладывается в заданный бюджет и время.",
            "all_routes": candidate_routes,
            "data_source": "SQLite database",
            "algorithm": algorithm_info
        }

    min_time = min(item["metrics"]["total_time"] for item in feasible_routes)
    max_route_time = max(item["metrics"]["total_time"] for item in feasible_routes)

    min_cost = min(item["metrics"]["total_cost"] for item in feasible_routes)
    max_cost = max(item["metrics"]["total_cost"] for item in feasible_routes)

    min_rating = min(item["metrics"]["average_rating"] for item in feasible_routes)
    max_rating = max(item["metrics"]["average_rating"] for item in feasible_routes)

    min_diversity = min(item["diversity_score"] for item in feasible_routes)
    max_diversity = max(item["diversity_score"] for item in feasible_routes)

    weights = get_weights(priority)

    for item in feasible_routes:
        metrics = item["metrics"]

        time_norm = normalize(metrics["total_time"], min_time, max_route_time)
        cost_norm = normalize(metrics["total_cost"], min_cost, max_cost)
        rating_norm = normalize(metrics["average_rating"], min_rating, max_rating)
        diversity_norm = normalize(item["diversity_score"], min_diversity, max_diversity)

        preference_norm = item["preference_score"]
        penalty_score = item["penalty_score"]

        raw_score = (
            weights["time"] * (1 - time_norm) +
            weights["cost"] * (1 - cost_norm) +
            weights["preferences"] * preference_norm +
            weights["rating"] * rating_norm +
            weights["diversity"] * diversity_norm -
            weights["penalty"] * penalty_score
        )

        score = max(0, min(raw_score, 1))

        item["calculation"] = {
            "time_norm": round(time_norm, 3),
            "cost_norm": round(cost_norm, 3),
            "preference_norm": round(preference_norm, 3),
            "rating_norm": round(rating_norm, 3),
            "diversity_norm": round(diversity_norm, 3),
            "penalty_score": round(penalty_score, 3),
            "weights": weights,
            "score_formula": (
                "Score(R) = "
                "w_time*(1-T*) + "
                "w_cost*(1-C*) + "
                "w_preferences*P* + "
                "w_rating*Q* + "
                "w_diversity*D* - "
                "lambda*Penalty(R)"
            ),
            "score": round(score, 3),
            "score_percent": round(score * 100, 1)
        }

    feasible_routes.sort(
        key=lambda item: item["calculation"]["score"],
        reverse=True
    )

    best_route = feasible_routes[0]

    calculation_explanation = build_calculation_explanation(
        best_route=best_route,
        feasible_routes_count=len(feasible_routes),
        candidate_routes_count=len(candidate_routes)
    )

    return {
        "status": "success",
        "data_source": "SQLite database",
        "best_route": best_route,
        "alternative_routes": feasible_routes[1:],
        "all_feasible_routes": feasible_routes,
        "algorithm": algorithm_info,
        "calculation_explanation": calculation_explanation,
        "math_model": {
            "graph": "G = (V, E)",
            "objective_function": (
                "Score(R) = "
                "w1*(1-T*) + "
                "w2*(1-C*) + "
                "w3*P* + "
                "w4*Q* + "
                "w5*D* - "
                "lambda*Penalty(R)"
            ),
            "criteria": {
                "T*": "нормализованное время маршрута",
                "C*": "нормализованная стоимость маршрута",
                "P*": "совпадение маршрута с предпочтениями пользователя",
                "Q*": "нормализованный рейтинг маршрута",
                "D*": "разнообразие категорий маршрута",
                "Penalty(R)": "штраф за приближение к ограничениям"
            },
            "constraints": [
                "T(R) <= T_max",
                "C(R) <= B"
            ],
            "description": (
                "Маршрут рассматривается как путь в неориентированном взвешенном графе. "
                "Вершины графа — города, рёбра — возможные переезды между ними. "
                "Данные о вершинах и рёбрах загружаются из SQLite-базы данных. "
                "Для оценки маршрута используется расширенная многокритериальная функция "
                "с учётом времени, стоимости, предпочтений, рейтинга, разнообразия и штрафа."
            )
        }
    }