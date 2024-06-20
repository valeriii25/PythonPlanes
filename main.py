import json
from contextlib import asynccontextmanager
from io import BytesIO
from uuid import UUID

from fastapi import FastAPI
from starlette.responses import StreamingResponse

from database import create_tables, delete_tables
from planes_router import router as planes_router, get_all_planes
from flights_router import router as flights_router, get_all_flights


@asynccontextmanager
async def lifespan(application: FastAPI):
    await create_tables()
    print("База готова")
    yield
    # await delete_tables()
    # print("База очищена")


app = FastAPI(lifespan=lifespan)
app.include_router(planes_router)
app.include_router(flights_router)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


@app.get("/export")
async def export_data():
    output = BytesIO()
    planes = await get_all_planes()
    flights = await get_all_flights()
    result = {'planes': [x.dict() for x in planes], 'flights': [x.dict() for x in flights]}
    print(json.dumps(result, cls=UUIDEncoder))
    output.write(json.dumps(result, cls=UUIDEncoder).encode())
    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="All_data.json"'
    }
    return StreamingResponse(output, headers=headers)
