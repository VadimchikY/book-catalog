from fastapi import APIRouter, Depends, status

from book.depends import get_book_usecase
from book.schemas import *
from book.use_cases import BookUseCase

book_router = APIRouter(tags=["book"], prefix="/book")


@book_router.post("/reserve")
async def reserve_book(reservation: ReservationRequest, book_usecase: BookUseCase = Depends(get_book_usecase)):
    await book_usecase.reserve_book(reservation)
    return {"message": "Book reserved successfully"}


@book_router.post("/return")
async def return_book(book_id: int, book_usecase: BookUseCase = Depends(get_book_usecase)):
    await book_usecase.return_book(book_id)
    return {"message": "Book returned successfully"}


@book_router.get("/", response_model=List[Book])
async def get_books(book_usecase: BookUseCase = Depends(get_book_usecase)):
    return await book_usecase.get_all_books()


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookBase, book_usecase: BookUseCase = Depends(get_book_usecase)):
    return await book_usecase.create_book(new_book)


@book_router.delete("/")
async def delete_book(book: DeleteBook, book_usecase: BookUseCase = Depends(get_book_usecase)):
    await book_usecase.delete_book(book.book_id)


@book_router.patch("/", response_model=Book)
async def update_book(book: Book, book_usecase: BookUseCase = Depends(get_book_usecase)):
    return await book_usecase.update_book(book)


@book_router.put("/{book_id}/genres/")
async def update_genres_to_book(book_id: int, genre_list: GenreList, book_usecase: BookUseCase = Depends(get_book_usecase)):
    await book_usecase.update_genres(book_id, genre_list.genres)


@book_router.get("/{book_id}", response_model=ExtendBook)
async def get_extend_book(book_id: int, book_usecase: BookUseCase = Depends(get_book_usecase)):
    return await book_usecase.get_extend_book(book_id)