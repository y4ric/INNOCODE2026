from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String, nullable=False)

    author: Mapped[str] = mapped_column(String, nullable=False)

    profile_pic : Mapped[str] = mapped_column(String, nullable=False)
class Cars(Base):
    __tablename__ = "cars"

    car_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    short_description: Mapped[str] = mapped_column(String, nullable=False)

    full_description: Mapped[str] = mapped_column(String, nullable=False)

    url_picture: Mapped[str] = mapped_column(String, nullable=False)
class Favorites(Base):
    __tablename__ = "favorites"

    car_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
