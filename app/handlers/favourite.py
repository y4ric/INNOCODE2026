from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.car import  AddFavouriteCar
from app.services.favourite_service import FavouriteService


router = APIRouter(
    prefix="/favorites",
    tags=["favorite"],
)

def favourite_service(
    db: Session = Depends(get_db),
) -> FavouriteService:
    return FavouriteService(db)
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def add_favourite(
    schema: AddFavouriteCar,
    service: FavouriteService = Depends(favourite_service),
):
    return service.add_favourite(schema, user_id=schema.user_id)

@router.get("/")
def get_favorites(
    user_id: int,  # 1. Говорим FastAPI, что ждём user_id от фронтенда
    service: FavouriteService = Depends(favourite_service),
):
    # 2. ИСПРАВЛЕНО: передаем user_id в метод сервиса!
    return service.get_favourites(user_id=user_id)

@router.delete("/")
def remove_favourite(
    car_id: int,
    user_id: int,
    service: FavouriteService = Depends(favourite_service),
):
    return service.remove_favourite(car_id=car_id, user_id=user_id)

