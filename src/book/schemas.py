from typing import List, Optional

from pydantic import BaseModel

from author.schemas import Author
from genre.schemas import Genre
from user.schemas import User


class BookBase(BaseModel):
    title: str
    price: float
    pages: int
    author_id: int


class DeleteBook(BaseModel):
    book_id: int


class Book(BookBase):
    book_id: int
    user_id: Optional[int] = None
    task_id: Optional[str] = None

    class Config:
        from_attributes = True


class ExtendBook(BaseModel):
    book_id: int
    title: str
    price: float
    pages: int
    author: Author
    genres: List[Genre]
    user: Optional[User] = None

    class Config:
        from_attributes = True


class ReservationRequest(BaseModel):
    user_id: int
    book_id: int
    days: int


class GenreList(BaseModel):
    genres: List[int]


class BookFilter(BaseModel):
    author_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
