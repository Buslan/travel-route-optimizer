from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class Place(Base):
    """
    Таблица places хранит вершины графа.

    Каждая вершина — это город или туристическая точка.
    Для каждой точки храним параметры, которые используются
    в математической модели маршрута.
    """

    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, index=True, nullable=False)
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)

    country = Column(String, default="Netherlands")

    rating = Column(Float, nullable=False)
    visit_cost = Column(Float, nullable=False)
    visit_time = Column(Float, nullable=False)

    categories = Column(String, nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    outgoing_edges = relationship(
        "Edge",
        foreign_keys="Edge.from_place_id",
        back_populates="from_place"
    )

    incoming_edges = relationship(
        "Edge",
        foreign_keys="Edge.to_place_id",
        back_populates="to_place"
    )


class Edge(Base):
    """
    Таблица edges хранит рёбра графа.

    Ребро показывает возможность перемещения между двумя вершинами.
    У каждого ребра есть веса:
    - расстояние;
    - время;
    - стоимость.
    """

    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)

    from_place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    to_place_id = Column(Integer, ForeignKey("places.id"), nullable=False)

    distance = Column(Float, nullable=False)
    travel_time = Column(Float, nullable=False)
    travel_cost = Column(Float, nullable=False)

    transport_type = Column(String, default="train")

    from_place = relationship(
        "Place",
        foreign_keys=[from_place_id],
        back_populates="outgoing_edges"
    )

    to_place = relationship(
        "Place",
        foreign_keys=[to_place_id],
        back_populates="incoming_edges"
    )


class SavedRoute(Base):
    """
    Таблица saved_routes хранит рассчитанные маршруты.

    Это нужно, чтобы проект выглядел как полноценное веб-приложение:
    пользователь может рассчитать маршрут, а система сохраняет результат.
    """

    __tablename__ = "saved_routes"

    id = Column(Integer, primary_key=True, index=True)

    route_name = Column(String, nullable=False)
    start_place = Column(String, nullable=False)
    finish_place = Column(String, nullable=False)

    total_distance = Column(Float, nullable=False)
    total_time = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)

    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    points = relationship(
        "SavedRoutePoint",
        back_populates="route",
        cascade="all, delete-orphan"
    )


class SavedRoutePoint(Base):
    """
    Таблица saved_route_points хранит точки внутри сохранённого маршрута.
    """

    __tablename__ = "saved_route_points"

    id = Column(Integer, primary_key=True, index=True)

    route_id = Column(Integer, ForeignKey("saved_routes.id"), nullable=False)
    place_code = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)

    route = relationship(
        "SavedRoute",
        back_populates="points"
    )