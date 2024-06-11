from typing import List, Optional

from pydantic import BaseModel

from author.schemas import Author
from genre.schemas import Genre


class BookBase(BaseModel):
    title: str
    price: float
    pages: int
    author_id: int
    genres: List[int] = []


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class DeleteBook(BaseModel):
    book_id: int


class Book(BookBase):
    book_id: int
    user_id: Optional[int] = None
    author: Author
    genres: List[Genre] = []
    task_id: Optional[str] = None

    class Config:
        from_attributes=True


class ReservationRequest(BaseModel):
    user_id: int
    book_id: int
    days: int