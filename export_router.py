from fastapi import APIRouter
import json
from io import BytesIO
from starlette.responses import StreamingResponse
from routers.planes_router import get_all_planes
from routers.flights_router import get_all_flights
from uuid_encoder import UUIDEncoder

router = APIRouter(
    prefix="/export",
    tags=["Запись в JSON"],
)


@router.get("")
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
