from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routers.planes_router import router as planes_router
from routers.flights_router import router as flights_router
from export_router import router as export_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(planes_router)
app.include_router(flights_router)
app.include_router(export_router)
