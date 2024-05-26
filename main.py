from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.dependencies import db_manager
from app.routes import user, chatbot_streaming , jwt_route
from contextlib import asynccontextmanager


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @asynccontextmanager
# async def lifespan_db():
#     await db_manager.connect_and_init_db()
#     try:
#         yield
#     finally:
#         await db_manager.connect_and_init_db()


@app.on_event("startup")
async def startup_event():
    await db_manager.connect_and_init_db()


@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.close_db_connect()



app.include_router(
    user.router,
    prefix='/api'
)

app.include_router(
    chatbot_streaming.router,
    prefix='/api'
)

app.include_router(
    jwt_route.router,
    prefix='/api'
)


# @app.exception_handler(BadRequest)
# async def bad_request_handler(req: Request, exc: BadRequest) -> JSONResponse:
#     return exc.gen_err_resp()


# @app.exception_handler(RequestValidationError)
# async def invalid_req_handler(
#         req: Request,
#         exc: RequestValidationError
# ) -> JSONResponse:
#     return JSONResponse(
#         status_code=400,
#         content={
#             "type": "about:blank",
#             'title': 'Bad Request',
#             'status': 400,
#             'detail': [str(exc)]
#         }
#     )


# @app.exception_handler(UnprocessableError)
# async def unprocessable_error_handler(
#         req: Request,
#         exc: UnprocessableError
# ) -> JSONResponse:
#     return exc.gen_err_resp()



from app.database.dependencies import get_database
from fastapi import APIRouter, Depends
from app.services.database import create_user , get_user , get_user_by_username
router = APIRouter()


@router.post("/test")
async def test(db: AsyncIOMotorClient = Depends(get_database)):
    logging.info("test")


@router.get("/test-non-blocking")
async def test():
    return "non-blocking"


app.include_router(
    router,
    prefix='/api'
)


