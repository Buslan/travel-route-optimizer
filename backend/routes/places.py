from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.repositories.place_repository import PlaceRepository


router = APIRouter(
    prefix="/db",
    tags=["Places"]
)


@router.get("/places")
def get_places_from_db(db: Session = Depends(get_db)):
    """
    Возвращает список городов из базы данных.

    Endpoint не обращается к SQLAlchemy напрямую.
    Для работы с таблицей places используется PlaceRepository.
    """

    repository = PlaceRepository(db)
    places = repository.get_all()

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