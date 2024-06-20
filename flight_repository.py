from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import FlightSchema, new_session, PlaneSchema
from flight_models import FlightDto, Flight
from plane_models import Plane


class FlightRepository:
    @classmethod
    async def add_flight(cls, flight: FlightDto) -> UUID:
        async with (new_session() as session):
            data = flight.model_dump()
            query = select(FlightSchema).filter_by(
                begin_airport=data['begin_airport']).filter_by(
                end_airport=data['end_airport'])
            result = await session.execute(query)
            existing_flight = result.scalar_one_or_none()
            if existing_flight is not None:
                raise ValueError
            new_flight = FlightSchema(**data)
            new_flight.id = uuid4()
            session.add(new_flight)
            await session.flush()
            await session.commit()
            return new_flight.id

    @classmethod
    async def edit_flight(cls, flight_id: UUID, flight: FlightDto) -> Flight:
        async with (new_session() as session):
            data = flight.model_dump()
            query = select(FlightSchema).options(
                joinedload(FlightSchema.suitable_planes)).filter_by(id=flight_id)
            result = await session.execute(query)
            flight_to_change = result.unique().scalar_one()
            for key, value in data.items():
                setattr(flight_to_change, key, value)
            await session.commit()
            return Flight.from_orm(flight_to_change)

    @classmethod
    async def delete_flight(cls, flight_id: UUID) -> Flight:
        async with (new_session() as session):
            query = select(FlightSchema).filter_by(id=flight_id)
            result = await session.execute(query)
            flight_to_delete = result.scalar_one()
            await session.delete(flight_to_delete)
            await session.commit()
            return Flight.from_orm(flight_to_delete)

    @classmethod
    async def get_flights(cls) -> list[Flight]:
        async with (new_session() as session):
            query = select(FlightSchema).options(joinedload(FlightSchema.suitable_planes))
            result = await session.execute(query)
            flight_models = result.scalars().unique().all()
            return [Flight.from_orm(x) for x in flight_models]

    @classmethod
    async def add_plane(cls, flight_id: UUID, plane_id: UUID) -> Flight:
        async with (new_session() as session):
            flight_query = select(FlightSchema).options(
                joinedload(FlightSchema.suitable_planes)).filter_by(id=flight_id)
            result = await session.execute(flight_query)
            flight_to_change = result.unique().scalar_one_or_none()
            if flight_to_change is None:
                raise ValueError('Flight is not found')
            plane_query = select(PlaneSchema).filter_by(id=plane_id)
            result = await session.execute(plane_query)
            plane_to_add = result.scalar_one_or_none()
            if plane_to_add is None:
                raise ValueError('Plane is not found')
            if plane_to_add in flight_to_change.suitable_planes:
                raise ValueError('Flight already contains this plane')
            if plane_to_add.max_capacity < flight_to_change.passengers:
                raise ValueError('Plane capacity is smaller than needed')
            if plane_to_add.max_distance < flight_to_change.distance:
                raise ValueError('Plane distance is smaller than needed')
            if plane_to_add.current_fuel < plane_to_add.fuel_consumption * flight_to_change.distance:
                raise ValueError('Current fuel is smaller than needed')
            flight_to_change.suitable_planes.append(plane_to_add)
            await session.commit()
            return Flight.from_orm(flight_to_change)

    @classmethod
    async def delete_plane(cls, flight_id: UUID, plane_id: UUID) -> Flight:
        async with (new_session() as session):
            flight_query = select(FlightSchema).options(
                joinedload(FlightSchema.suitable_planes)).filter_by(
                id=flight_id)
            result = await session.execute(flight_query)
            flight_to_change = result.unique().scalar_one_or_none()
            if flight_to_change is None:
                raise ValueError('Flight is not found')
            plane_query = select(PlaneSchema).filter_by(id=plane_id)
            result = await session.execute(plane_query)
            plane_to_delete = result.scalar_one_or_none()
            if plane_to_delete is None:
                raise ValueError('Plane is not found')
            if plane_to_delete not in flight_to_change.suitable_planes:
                raise ValueError('Flight does not contain this plane')
            flight_to_change.suitable_planes.remove(plane_to_delete)
            await session.commit()
            return Flight.from_orm(flight_to_change)

    @classmethod
    async def get_available_planes_by_capacity(cls, flight_id: UUID) -> list[Plane]:
        async with (new_session() as session):
            flight_query = select(FlightSchema).filter_by(id=flight_id)
            result = await session.execute(flight_query)
            flight_to_change = result.scalar_one()
            plane_query = select(PlaneSchema).where(
                PlaneSchema.max_capacity >= flight_to_change.passengers)
            result = await session.execute(plane_query)
            available_planes = [Plane.from_orm(x) for x in result.scalars().all()]
            return available_planes

    @classmethod
    async def get_available_planes_by_distance(cls, flight_id: UUID) -> list[Plane]:
        async with (new_session() as session):
            flight_query = select(FlightSchema).filter_by(id=flight_id)
            result = await session.execute(flight_query)
            flight_to_change = result.scalar_one()
            plane_query = select(PlaneSchema).where(
                PlaneSchema.max_distance >= flight_to_change.distance)
            result = await session.execute(plane_query)
            available_planes = [Plane.from_orm(x) for x in result.scalars().all()]
            return available_planes

    @classmethod
    async def conduct_flight(cls, flight_id: UUID) -> Flight:
        async with (new_session() as session):
            flight_query = select(FlightSchema).options(
                joinedload(FlightSchema.suitable_planes)).filter_by(
                id=flight_id)
            result = await session.execute(flight_query)
            flight_to_change = result.unique().scalar_one_or_none()
            if flight_to_change is None:
                raise ValueError('Flight is not found')
            if not flight_to_change.suitable_planes:
                raise ValueError('Flight does not contain any planes')
            for plane in flight_to_change.suitable_planes:
                plane.current_fuel = plane.current_fuel - plane.fuel_consumption * flight_to_change.distance
                if plane.current_fuel < plane.fuel_consumption * flight_to_change.distance:
                    flight_to_change.suitable_planes.remove(plane)
            await session.commit()
            return Flight.from_orm(flight_to_change)
