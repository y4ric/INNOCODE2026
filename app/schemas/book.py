from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    user_id : int = Field()
    name: str = Field(min_length=1, max_length=200)
    profile_pic: str = Field(min_length=1, max_length=200)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=200)


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    profile_pic: str