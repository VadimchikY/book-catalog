from datetime import datetime, timedelta

from book.repository import BookRepository
from book.schemas import BookBase, Book, ReservationRequest
from core.exceptions import AlreadyReseved
from tasks import return_book


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

    async def reserve_book(self, reservation: ReservationRequest):
        eta = datetime.now() + timedelta(days=reservation.days)
        task_id = return_book.apply_async(args=[reservation.book_id], eta=eta)
        await self.repo.reserve_book(reservation.book_id, reservation.user_id, task_id)

    async def return_book(self, book_id: int):
        task_id = await self.repo.restore_user(book_id)
        return_book.AsyncResult(task_id).revoke()
