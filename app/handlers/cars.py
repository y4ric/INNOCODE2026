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
    "/{car_id}",
    response_model=CarResponse,
)
def get_car(
    car_id: int,
    service: CarService = Depends(get_car_service),
):
    return service.get_car(car_id)

@router.get(
    "/",
    response_model=list[CarResponse],
)
def get_cars(
    service: CarService = Depends(get_car_service),
):
    return service.get_cars()
@router.put("/{car_id}")
def update_car(
    car_id: int,
    schema: CarCreate,  # или ваша специальная схема для обновления, например CarUpdate
    service: CarService = Depends(get_car_service),
):
    return service.update_car(car_id, schema)
