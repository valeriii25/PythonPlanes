from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from plane_repository import PlaneRepository
from plane_models import Plane, PlaneDto

router = APIRouter(
    prefix="/planes",
    tags=["Самолеты"],
)


@router.post("")
async def add_plane(plane: PlaneDto) -> dict[str, UUID]:
    try:
        new_plane_id = await PlaneRepository.add_plane(plane)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    return {"id": new_plane_id}


@router.put("/{plane_id}")
async def edit_plane(plane_id: UUID, plane: PlaneDto) -> Plane:
    try:
        edited_plane = await PlaneRepository.edit_plane(plane_id, plane)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Plane is not found")
    return edited_plane


@router.delete("/{plane_id}")
async def delete_plane(plane_id: UUID) -> Plane:
    try:
        deleted_plane = await PlaneRepository.delete_plane(plane_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Plane is not found")
    return deleted_plane


@router.get("")
async def get_all_planes() -> list[Plane]:
    planes = await PlaneRepository.get_planes()
    return planes


@router.get("/capacity/average")
async def get_average_plane_capacity() -> int:
    try:
        average_capacity = await PlaneRepository.get_average_capacity()
    except ZeroDivisionError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return average_capacity


@router.get("/distance/average")
async def get_average_plane_distance() -> int:
    try:
        average_distance = await PlaneRepository.get_average_distance()
    except ZeroDivisionError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return average_distance


@router.get("/capacity/maximum")
async def get_most_capacious_plane() -> int:
    try:
        max_capacity = await PlaneRepository.get_max_capacity()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return max_capacity


@router.get("/distance/maximum")
async def get_most_beneficial_plane() -> int:
    try:
        max_distance = await PlaneRepository.get_max_distance()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return max_distance
