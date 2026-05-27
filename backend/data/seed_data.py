from math import radians, sin, cos, sqrt, atan2

from backend.database import SessionLocal, create_tables
from backend.models import Place, Edge


PLACES_DATA = [
    {
        "code": "Moscow",
        "name_ru": "Москва",
        "name_en": "Moscow",
        "country": "Russia",
        "rating": 4.8,
        "visit_cost": 55,
        "visit_time": 7,
        "categories": "culture,history,architecture,food",
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    {
        "code": "Saint Petersburg",
        "name_ru": "Санкт-Петербург",
        "name_en": "Saint Petersburg",
        "country": "Russia",
        "rating": 4.9,
        "visit_cost": 60,
        "visit_time": 8,
        "categories": "culture,history,architecture,art",
        "latitude": 59.9311,
        "longitude": 30.3609
    },
    {
        "code": "Smolensk",
        "name_ru": "Смоленск",
        "name_en": "Smolensk",
        "country": "Russia",
        "rating": 4.3,
        "visit_cost": 30,
        "visit_time": 4,
        "categories": "history,culture,architecture",
        "latitude": 54.7826,
        "longitude": 32.0453
    },
    {
        "code": "Paris",
        "name_ru": "Париж",
        "name_en": "Paris",
        "country": "France",
        "rating": 4.9,
        "visit_cost": 95,
        "visit_time": 9,
        "categories": "culture,architecture,art,food",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    {
        "code": "New York",
        "name_ru": "Нью-Йорк",
        "name_en": "New York",
        "country": "USA",
        "rating": 4.8,
        "visit_cost": 120,
        "visit_time": 10,
        "categories": "modern,architecture,food,art",
        "latitude": 40.7128,
        "longitude": -74.0060
    },
    {
        "code": "Sochi",
        "name_ru": "Сочи",
        "name_en": "Sochi",
        "country": "Russia",
        "rating": 4.6,
        "visit_cost": 50,
        "visit_time": 6,
        "categories": "sea,nature,food,relax",
        "latitude": 43.5855,
        "longitude": 39.7231
    },
    {
        "code": "Tambov",
        "name_ru": "Тамбов",
        "name_en": "Tambov",
        "country": "Russia",
        "rating": 4.1,
        "visit_cost": 25,
        "visit_time": 3,
        "categories": "history,culture,food",
        "latitude": 52.7212,
        "longitude": 41.4523
    },
    {
        "code": "Berlin",
        "name_ru": "Берлин",
        "name_en": "Berlin",
        "country": "Germany",
        "rating": 4.7,
        "visit_cost": 80,
        "visit_time": 8,
        "categories": "history,modern,culture,architecture",
        "latitude": 52.5200,
        "longitude": 13.4050
    },
    {
        "code": "Gelendzhik",
        "name_ru": "Геленджик",
        "name_en": "Gelendzhik",
        "country": "Russia",
        "rating": 4.4,
        "visit_cost": 42,
        "visit_time": 5,
        "categories": "sea,nature,relax,food",
        "latitude": 44.5622,
        "longitude": 38.0848
    },
    {
        "code": "Istanbul",
        "name_ru": "Стамбул",
        "name_en": "Istanbul",
        "country": "Turkey",
        "rating": 4.8,
        "visit_cost": 70,
        "visit_time": 8,
        "categories": "history,culture,architecture,food,sea",
        "latitude": 41.0082,
        "longitude": 28.9784
    },
    {
        "code": "Magadan",
        "name_ru": "Магадан",
        "name_en": "Magadan",
        "country": "Russia",
        "rating": 4.2,
        "visit_cost": 65,
        "visit_time": 5,
        "categories": "nature,history,adventure",
        "latitude": 59.5682,
        "longitude": 150.8086
    }
]


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """
    Приближённый расчёт расстояния между двумя точками по координатам.
    Используется формула гаверсинуса.
    """

    earth_radius_km = 6371

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


def estimate_travel_time(distance_km):
    """
    Учебная модель оценки времени перемещения.

    Для близких маршрутов считаем среднюю скорость ниже,
    для дальних — выше, как имитацию самолёта/поезда.
    """

    if distance_km < 400:
        speed = 90
        extra_time = 1
    elif distance_km < 1500:
        speed = 250
        extra_time = 2
    else:
        speed = 750
        extra_time = 4

    return round(distance_km / speed + extra_time, 2)


def estimate_travel_cost(distance_km):
    """
    Учебная модель оценки стоимости перемещения.

    Стоимость считается приблизительно, чтобы алгоритм мог сравнивать маршруты.
    """

    if distance_km < 400:
        base_cost = 15
        coefficient = 0.08
    elif distance_km < 1500:
        base_cost = 45
        coefficient = 0.10
    else:
        base_cost = 110
        coefficient = 0.07

    return round(base_cost + distance_km * coefficient, 2)


def generate_edges_data():
    """
    Генерирует полный неориентированный граф между всеми городами.
    В базу записываем по одному ребру между каждой парой городов.
    """

    edges = []

    for i in range(len(PLACES_DATA)):
        for j in range(i + 1, len(PLACES_DATA)):
            from_place = PLACES_DATA[i]
            to_place = PLACES_DATA[j]

            distance = haversine_distance_km(
                from_place["latitude"],
                from_place["longitude"],
                to_place["latitude"],
                to_place["longitude"]
            )

            distance = round(distance, 2)
            travel_time = estimate_travel_time(distance)
            travel_cost = estimate_travel_cost(distance)

            edges.append(
                (
                    from_place["code"],
                    to_place["code"],
                    distance,
                    travel_time,
                    travel_cost
                )
            )

    return edges


def seed_places(db):
    existing_count = db.query(Place).count()

    if existing_count > 0:
        print("Places already exist. Skipping places seeding.")
        return

    for place_data in PLACES_DATA:
        place = Place(**place_data)
        db.add(place)

    db.commit()
    print("Places inserted successfully.")


def seed_edges(db):
    existing_count = db.query(Edge).count()

    if existing_count > 0:
        print("Edges already exist. Skipping edges seeding.")
        return

    places = {
        place.code: place
        for place in db.query(Place).all()
    }

    edges_data = generate_edges_data()

    for from_code, to_code, distance, travel_time, travel_cost in edges_data:
        edge = Edge(
            from_place_id=places[from_code].id,
            to_place_id=places[to_code].id,
            distance=distance,
            travel_time=travel_time,
            travel_cost=travel_cost,
            transport_type="mixed"
        )

        db.add(edge)

    db.commit()
    print("Edges inserted successfully.")


def seed_database():
    create_tables()

    db = SessionLocal()

    try:
        seed_places(db)
        seed_edges(db)
        print("Database seeding completed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()