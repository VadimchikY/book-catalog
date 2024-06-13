import asyncio

from celery import Celery

from book.repository import BookRepository
from core.database_depends import get_db

celery_app = Celery('tasks', broker='redis://redis:6379/0')


def run_async(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        return asyncio.ensure_future(func(*args, **kwargs))
    else:
        return loop.run_until_complete(func(*args, **kwargs))


@celery_app.task
def return_book_task(book_id):
    async def _return_book_task(book_id):
        async with get_db() as session:
            repo = BookRepository(session)
            await repo.restore_user(book_id)

    return run_async(_return_book_task, book_id)
