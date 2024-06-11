from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.db import Base


class Author(Base):
    __tablename__ = "authors"
    author_id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["Book"]] = relationship(back_populates="author")
