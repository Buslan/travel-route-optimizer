from pydantic import BaseModel
from typing import List


class RouteOptimizationRequest(BaseModel):
    start: str
    finish: str
    stops: List[str]
    budget: float
    max_time: float
    preferences: List[str]
    priority: str