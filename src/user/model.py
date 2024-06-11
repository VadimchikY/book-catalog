from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.db import Base


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    avatar: Mapped[str] = mapped_column()

    books: Mapped[List["Book"]] = relationship(back_populates="user")
