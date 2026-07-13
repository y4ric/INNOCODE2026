from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.book import Book
from repositories.book_repository import BookRepository
from schemas.book import  BookUpdate
from schemas.book import CarCreate
from models.book import Cars



class FavouriteService:

    def __init__(self, repository):
        self.repository = repository

    def add_favourite(self, car_id: int) -> Cars:
        favourite_car = Cars(
            car_id=car_id
        )
        self.repository.add(favourite_car)
        return {"status": "success", "message": "Ваша машина успешно добавлена в избранное"}

