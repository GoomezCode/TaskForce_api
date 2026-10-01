from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


class TaskNotFoundError(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )


class TaskAlreadyExistsError(HTTPException):
    def __init__(self, title: str):
        super().__init__(
            status_code=409,
            detail=f"Task '{title}' already exists",
        )


def add_exception_handlers(app: FastAPI) -> None:
    """Add global exception handlers."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "code": exc.__class__.__name__},
        )
