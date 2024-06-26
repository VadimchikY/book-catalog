from fastapi import FastAPI
from author.router import author_router
from book.router import book_router
from core.exception_handler import include_exceptions_to_app
from genre.router import genre_router
from user.router import user_router

app = FastAPI()

include_exceptions_to_app(app)
app.include_router(author_router)
app.include_router(book_router)
app.include_router(genre_router)
app.include_router(user_router)


@app.get("/healthcheck")
def health():
    return {"message": "service is available"}
