from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.database import create_tables
from server.api.plane.resources import router as planes_router
from server.api.flight.resources import router as flights_router
from server.api.export.resources import router as export_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(planes_router)
app.include_router(flights_router)
app.include_router(export_router)
