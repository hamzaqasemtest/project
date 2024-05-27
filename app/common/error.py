import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ItemNotFoundException(CustomException):
    def __init__(self, item_id: int):
        super().__init__(status_code=404, detail=f"Item with ID {item_id} not found.")


async def custom_exception_handler(request: Request, exc: CustomException):
    logging.error(f"CustomException: {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "path": request.url.path},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled Exception: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "path": request.url.path},
    )
