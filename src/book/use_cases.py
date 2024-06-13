from datetime import datetime, timedelta
from typing import List

from book.repository import BookRepository
from book.schemas import BookBase, Book, ReservationRequest
from tasks import return_book_task


class BookUseCase:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def create_book(self, book: BookBase):
        return await self.repo.create_book(book)

    async def update_book(self, book: Book):
        return await self.repo.update_book(book)

    async def get_all_books(self):
        return await self.repo.get_all_books()

    async def get_book(self, book_id: int):
        return await self.repo.get_book(book_id)

    async def delete_book(self, book_id: int):
        await self.repo.delete_book(book_id)

    async def update_genres(self, book_id: int, genres: List):
        await self.repo.update_genres(book_id, genres)


    async def reserve_book(self, reservation: ReservationRequest):
        eta = datetime.now() + timedelta(days=reservation.days)
        task = return_book_task.apply_async(args=[reservation.book_id], eta=eta)
        task_id = task.id
        await self.repo.reserve_book(reservation.book_id, reservation.user_id, task_id)

    async def return_book(self, book_id: int):
        task_id = await self.repo.restore_user(book_id)
        return_book_task.AsyncResult(task_id).revoke()
