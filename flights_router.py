from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from flight_repository import FlightRepository
from flight_models import Flight, FlightDto
from plane_models import Plane

router = APIRouter(
    prefix="/flights",
    tags=["Рейсы"],
)


@router.post("")
async def add_flight(flight: FlightDto) -> dict[str, UUID]:
    try:
        new_flight_id = await FlightRepository.add_flight(flight)
    except ValueError:
        raise HTTPException(status_code=400, detail="Flight already exists")
    return {"id": new_flight_id}


@router.put("/{flight_id}")
async def edit_flight(flight_id: UUID, flight: FlightDto) -> Flight:
    try:
        edited_flight = await FlightRepository.edit_flight(flight_id, flight)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Flight is not found")
    return edited_flight


@router.patch("/{flight_id}/add")
async def add_plane_to_flight(flight_id: UUID, plane_id: UUID) -> Flight:
    try:
        edited_flight = await FlightRepository.add_plane(flight_id, plane_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return edited_flight


@router.patch("/{flight_id}/delete")
async def delete_plane_from_flight(flight_id: UUID, plane_id: UUID) -> Flight:
    try:
        edited_flight = await FlightRepository.delete_plane(flight_id, plane_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return edited_flight


@router.delete("/{flight_id}")
async def delete_flight(flight_id: UUID) -> Flight:
    try:
        deleted_flight = await FlightRepository.delete_flight(flight_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Flight is not found")
    return deleted_flight


@router.get("")
async def get_all_flights() -> list[Flight]:
    flights = await FlightRepository.get_flights()
    return flights


@router.get("/{flight_id}/capacity")
async def get_available_planes_by_capacity(flight_id: UUID) -> list[Plane]:
    try:
        planes = await FlightRepository.get_available_planes_by_capacity(flight_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Flight is not found")
    return planes


@router.get("/{flight_id}/distance")
async def get_available_planes_by_distance(flight_id: UUID) -> list[Plane]:
    try:
        planes = await FlightRepository.get_available_planes_by_distance(flight_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Flight is not found")
    return planes


@router.post("/{flight_id}")
async def conduct_flight(flight_id: UUID) -> Flight:
    try:
        conducted_flight = await FlightRepository.conduct_flight(flight_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    return conducted_flight
