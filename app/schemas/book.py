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
    full_description: str = Field(default=None, min_length=1, max_length=200)
    url_picture: str = Field(default=None, min_length=1, max_length=200)
class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    short_description: str
    full_description: str
    url_picture: str
class AddFavouriteCar(BaseModel):
    car_id: int = Field()
class FavouriteCarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    car_id: int