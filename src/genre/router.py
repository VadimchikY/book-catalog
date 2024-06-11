from typing import List

from fastapi import APIRouter, Depends, status

from genre.depends import get_genre_usecase
from genre.schemas import *
from genre.use_cases import GenreUseCase

genre_router = APIRouter(tags=["genre"], prefix="/genre")


@genre_router.get("/", response_model=List[Genre])
async def get_genres(genre_usecase: GenreUseCase = Depends(get_genre_usecase)):
    return await genre_usecase.get_all_genres()


@genre_router.post("/", response_model=Genre, status_code=status.HTTP_201_CREATED)
async def create_author(new_genre: BaseGenre, genre_usecase: GenreUseCase = Depends(get_genre_usecase)):
    return await genre_usecase.create_genre(new_genre)


@genre_router.delete("/")
async def delete_genre(genre: DeleteGenre, genre_usecase: GenreUseCase = Depends(get_genre_usecase)):
    await genre_usecase.delete_genre(genre.genre_id)


@genre_router.patch("/", response_model=Genre)
async def update_genre(genre: Genre, genre_usecase: GenreUseCase = Depends(get_genre_usecase)):
    return await genre_usecase.update_genre(genre)
