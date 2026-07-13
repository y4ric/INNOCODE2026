from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.book import  ProfileResponse, BookUpdate, CarCreate
from services.book_service import BookService
from schemas.book import CarCreate , AddFavouriteCar
from services.favourite_service import FavouriteService


router = APIRouter(
    prefix="/Favourite",
    tags=["favourite"],
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
    return service.add_favourite(schema)
