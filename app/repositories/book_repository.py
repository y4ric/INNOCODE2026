from sqlalchemy.orm import Session

from app.models.book import Book, Cars


class BookRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, book: Book) -> Book:
        return self._upsert(book)

    def update(self, book: Book) -> Book:
        return self._upsert(book)

    def _upsert(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        return book

    def get_all(self) -> list[Book]:
        return self.db.query(Book).all()

    def get_by_id(
        self,
        car_id: int,
    ) -> Cars | None:

        return (
            self.db.query(Cars).filter(Cars.car_id == car_id).first()
        )

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()