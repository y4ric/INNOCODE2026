from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.car import ProfileResponse, CarCreate, CarResponse
from app.services.car_service import CarService


router = APIRouter(
    prefix="/cars",
    tags=["car"],
)

def get_car_service(
    db: Session = Depends(get_db),
) -> CarService:
    return CarService(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_car(
    schema: CarCreate,
    service: CarService = Depends(get_car_service),
):
    return service.create_car(schema)


@router.get(
    "/",
    response_model=list[CarResponse],
)
def get_cars(
    service: CarService = Depends(get_car_service),
):
    return service.get_cars()
