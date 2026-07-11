from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import  BookUpdate
from app.schemas.book import CarCreate
from app.models.book import Cars



class FavouriteService:

    def __init__(self, repository):
        self.repository = repository

    def add_favourite(self, car_id: int) -> Cars:
        favourite_car = Cars(
            car_id=car_id
        )
        return self.repository.create(favourite_car)
