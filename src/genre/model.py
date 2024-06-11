from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.db import Base


class Genre(Base):
    __tablename__ = "genres"
    genre_id: Mapped[int] = mapped_column(primary_key=True)
    genre_name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["Book"]] = relationship(back_populates="genres", secondary="books_genres")

class BooksGenres(Base):
    __tablename__ = "books_genres"
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True)
