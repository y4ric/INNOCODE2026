from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cars(Base):
    __tablename__ = "cars"

    car_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    short_description: Mapped[str] = mapped_column(String, nullable=False)

    full_description: Mapped[str] = mapped_column(String, nullable=False)

    url_picture: Mapped[str] = mapped_column(String, nullable=False)


    views_count: Mapped[int] = mapped_column(default=0, nullable=False)
    favorites_count: Mapped[int] = mapped_column(default=0, nullable=False)



class Favorites(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    car_id: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column()
