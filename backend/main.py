from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import create_tables, get_db
from backend.models import Place, Edge, SavedRoute
from backend.schemas import RouteOptimizationRequest
from backend.services.route_optimizer import optimize_route_from_db
from backend.services.route_storage import save_optimized_route

app = FastAPI(
    title="Travel Route Optimizer",
    description="Веб-приложение для подбора маршрута путешествия через несколько точек",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
def home():
    return {
        "message": "Travel Route Optimizer API работает",
        "status": "ok",
        "data_source": "SQLite database"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "Travel Route Optimizer",
        "database": "connected"
    }


@app.get("/db/places")
def get_places_from_db(db: Session = Depends(get_db)):
    places = db.query(Place).all()

    return {
        "count": len(places),
        "places": [
            {
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
            for place in places
        ]
    }


@app.get("/db/edges")
def get_edges_from_db(db: Session = Depends(get_db)):
    edges = db.query(Edge).all()

    return {
        "count": len(edges),
        "edges": [
            {
                "id": edge.id,
                "from": edge.from_place.code,
                "to": edge.to_place.code,
                "distance": edge.distance,
                "travel_time": edge.travel_time,
                "travel_cost": edge.travel_cost,
                "transport_type": edge.transport_type
            }
            for edge in edges
        ]
    }


@app.get("/db/saved-routes")
def get_saved_routes(db: Session = Depends(get_db)):
    saved_routes = db.query(SavedRoute).order_by(SavedRoute.created_at.desc()).all()

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


@app.post("/optimize-route")
def optimize_route_endpoint(
    request: RouteOptimizationRequest,
    db: Session = Depends(get_db)
):
    result = optimize_route_from_db(
        db=db,
        start=request.start,
        finish=request.finish,
        stops=request.stops,
        budget=request.budget,
        max_time=request.max_time,
        preferences=request.preferences,
        priority=request.priority
    )

    saved_route_id = save_optimized_route(
        db=db,
        optimization_result=result
    )

    if saved_route_id:
        result["saved_route_id"] = saved_route_id

    return result