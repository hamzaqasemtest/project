from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db_manager
from contextlib import asynccontextmanager
from app.routes import RoutesIncluder
from app.common.error import custom_exception_handler, generic_exception_handler, CustomException

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

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(RoutesIncluder.get_routes())








from app.database import get_database
from fastapi import APIRouter, Depends
from app.services.database import create_user , get_user , get_user_by_username
router = APIRouter()
from motor.motor_asyncio import AsyncIOMotorClient

@router.post("/test")
async def test(db: AsyncIOMotorClient = Depends(get_database)):
    return get_user_by_username(db, "koko")

@router.get("/test-non-blocking")
async def test():
    return "non-blocking"


app.include_router(
    router,
    prefix='/api'
)


