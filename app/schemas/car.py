from pydantic import BaseModel, ConfigDict, Field


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=200)


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    profile_pic: str


class CarCreate(BaseModel):
    name: str = Field(default=None, min_length=1, max_length=200)
    short_description: str = Field(default=None, min_length=1, max_length=200)
    full_description: str = Field(default=None, min_length=1, max_length=1000)
    url_picture: str = Field(default=None, min_length=1, max_length=1000)


class CarResponse(BaseModel):
    car_id: int
    name: str
    short_description: str | None = None
    full_description: str | None = None
    url_picture: str | None = None

    # === ДОБАВИЛИ ОБЯЗАТЕЛЬНЫЕ ПОЛЯ ДЛЯ СТАТИСТИКИ ===
    views_count: int
    favorites_count: int

    class Config:
        from_attributes = True


class AddFavouriteCar(BaseModel):
    car_id: int = Field()
    user_id: int = Field()


class FavouriteCarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    car_id: int
    user_id: int
