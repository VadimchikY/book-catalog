from typing import List

from fastapi import APIRouter, Depends, status

from author.depends import get_author_usecase
from author.schemas import *
from author.use_cases import AuthorUseCase

author_router = APIRouter(tags=["author"], prefix="/author")


@author_router.get("/", response_model=List[Author])
async def get_authors(author_usecase: AuthorUseCase = Depends(get_author_usecase)):
    return await author_usecase.get_all_authors()


@author_router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(new_author: BaseAuthor, author_usecase: AuthorUseCase = Depends(get_author_usecase)):
    return await author_usecase.create_author(new_author)


@author_router.delete("/")
async def delete_author(author: DeleteAuthor, author_usecase: AuthorUseCase = Depends(get_author_usecase)):
    await author_usecase.delete_author(author.author_id)


@author_router.patch("/", response_model=Author)
async def update_author(author: Author, author_usecase: AuthorUseCase = Depends(get_author_usecase)):
    return await author_usecase.update_author(author)
