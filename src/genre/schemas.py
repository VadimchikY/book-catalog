from pydantic import BaseModel


class BaseGenre(BaseModel):
    genre_name: str

    class Config:
        from_attributes=True


class DeleteGenre(BaseModel):
    genre_id: int


class Genre(BaseGenre, DeleteGenre):
    pass
