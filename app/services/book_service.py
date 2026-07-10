from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import  BookUpdate
from app.schemas.book import CarCreate
from app.models.book import Cars


class BookService:

    def __init__(self, db: Session):
        self.repository = BookRepository(db)





    def create_car(self, schema: CarCreate) -> Cars:
        new_car = Cars(
            car_id = schema.car_id,
            name = schema.name,
            category = schema.category
        )
        return self.repository.create(new_car)


    def get_books(self) -> list[Cars]:
        return self.repository.get_all()

    def get_car(self, car_id: int) -> Cars:
        car = self.repository.get_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        return car

    def update_book(
            self,
            book_id: int,
            schema: BookUpdate,
    ) -> Book:

        book = self.get_book(book_id)

        if schema.title is None and schema.author is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            book.title = schema.title

        if schema.author is not None:
            book.author = schema.author

        return self.repository.update(book)

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)

        self.repository.delete(book)