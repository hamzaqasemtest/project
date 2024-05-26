from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class ItemNotFoundException(CustomException):
    def __init__(self, item_id: int):
        super().__init__(status_code=404, detail=f"Item with ID {item_id} not found.")

def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."},
    )
