from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db_manager
from contextlib import asynccontextmanager
from app.routes import RoutesIncluder

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print('startup')
#     yield
#     print('shutdown')


app = FastAPI(
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,  
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await db_manager.connect_and_init_db()


@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.close_db_connect()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/healthz")
async def healthz():
    return {"status": "healthy"}

app.include_router(RoutesIncluder.get_routes())


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



# from app.database import get_database
# from fastapi import APIRouter, Depends
# from app.services.database import create_user , get_user , get_user_by_username
# router = APIRouter()


# @router.post("/test")
# async def test(db: AsyncIOMotorClient = Depends(get_database)):
#     return await get_user_by_username(db, "koko")

# @router.get("/test-non-blocking")
# async def test():
#     return "non-blocking"


# app.include_router(
#     router,
#     prefix='/api'
# )


