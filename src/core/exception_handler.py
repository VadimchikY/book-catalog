from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from core.exceptions import (
    DatabaseConnectionException,
    DatabaseException,
    RequestProcessingException
)


async def request_processiong_exeption_handler(request: Request, exc: RequestProcessingException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": f"{str(exc)}"}
    )


async def database_exception_handler(
        request: Request, exc: DatabaseException | DatabaseConnectionException
) -> Response:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Please try later."})


def include_exceptions_to_app(app: FastAPI):
    app.add_exception_handler(RequestProcessingException, request_processiong_exeption_handler)
    app.add_exception_handler(DatabaseException, database_exception_handler)
    app.add_exception_handler(DatabaseConnectionException, database_exception_handler)
