import asyncio
from core.database_depends import get_sql_alchemy
from author.model import Author
from book.model import Book
from genre.model import Genre
from user.model import User


async def create_test_data() -> None:
    sqlalchemy = await get_sql_alchemy()
    async with sqlalchemy.session_maker() as session:
        author1 = Author(fullname="Александр Пушкин")
        author2 = Author(fullname="Лев Толстой")
        author3 = Author(fullname="Федор Достоевский")

        session.add_all([author1, author2, author3])

        # Создание жанров
        genre1 = Genre(genre_name="Роман")
        genre2 = Genre(genre_name="Поэзия")
        genre3 = Genre(genre_name="Драма")

        session.add_all([genre1, genre2, genre3])

        # Создание пользователей
        user1 = User(first_name="Иван", last_name="Иванов", avatar="avatar1.jpg")
        user2 = User(first_name="Петр", last_name="Петров", avatar="avatar2.jpg")

        session.add_all([user1, user2])
        await session.commit()
        # Создание книг
        book1 = Book(title="Евгений Онегин", price=500.0, pages=300, author_id=author1.author_id)
        book2 = Book(title="Война и мир", price=1200.0, pages=800, author_id=author2.author_id)
        book3 = Book(title="Преступление и наказание", price=800.0, pages=500, author_id=author3.author_id)

        book1.genres = [genre2, genre1]
        book2.genres = [genre1]
        book3.genres = [genre3]

        session.add_all([book1, book2, book3])
        await session.commit()


asyncio.run(create_test_data())
