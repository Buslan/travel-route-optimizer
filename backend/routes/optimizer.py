from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import RouteOptimizationRequest
from backend.services.route_optimizer import optimize_route_from_db
from backend.services.route_storage import save_optimized_route


router = APIRouter(
    tags=["Optimizer"]
)


@router.post("/optimize-route")
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