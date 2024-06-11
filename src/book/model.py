from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.db import Base



class Book(Base):
    __tablename__ = "books"
    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[float]
    pages: Mapped[int]
    task_id: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    user: Mapped[Optional["User"]] = relationship(back_populates="books")

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"))
    author: Mapped["Author"] = relationship(back_populates="books")

    genres: Mapped[List["Genre"]] = relationship(back_populates="books", secondary="books_genres")
