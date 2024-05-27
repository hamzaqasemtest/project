import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ItemNotFoundException(CustomException):
    def __init__(self, item_id: int):
        super().__init__(status_code=404, detail=f"Item with ID {item_id} not found.")

class UserAlreadyExistsException(CustomException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists.")

class RegistrationFailedException(CustomException):
    def __init__(self):
        super().__init__(status_code=500, detail="An error has occurred during registration.")

class InvalidCredentialsException(CustomException):
    def __init__(self):
        super().__init__(status_code=400, detail="Wrong username/password.")

async def custom_exception_handler(request: Request, exc: CustomException):
    logging.error(f"CustomException: {type(exc).__name__} - Path: {request.url.path} message: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "path": request.url.path},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled Exception type: {type(exc).__name__} - Path: {request.url.path} message: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "path": request.url.path},
    )
