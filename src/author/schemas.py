from pydantic import BaseModel


class BaseAuthor(BaseModel):
    fullname: str

    class Config:
        from_attributes=True


class DeleteAuthor(BaseModel):
    author_id: int


class Author(BaseAuthor, DeleteAuthor):
    pass
