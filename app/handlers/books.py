from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.book import  ProfileResponse, BookUpdate, CarCreate
from app.services.book_service import BookService


router = APIRouter(
    prefix="/cars",
    tags=["car"],
)

def get_book_service(
    db: Session = Depends(get_db),
) -> BookService:
    return BookService(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_car(
    schema: CarCreate,
    service: BookService = Depends(get_book_service),
):
    return service.create_car(schema)
@router.get(
    "/",
    response_model=list[ProfileResponse],
)
def get_books(
    service: BookService = Depends(get_book_service),
):
    return service.get_books()
@router.get(
    "/{book_id}",

)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    return service.get_book(book_id)
@router.patch(
    "/{book_id}",
    response_model=ProfileResponse,
)
def update_book(
    book_id: int,
    schema: BookUpdate,
    service: BookService = Depends(get_book_service),
):
    return service.update_book(book_id, schema)
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
) -> None:
    service.delete_book(book_id)