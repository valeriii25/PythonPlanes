from uuid import UUID, uuid4
from sqlalchemy import select
from database import PlaneSchema, new_session
from models.plane_models import PlaneDto, Plane


class PlaneRepository:
    @classmethod
    async def add_plane(cls, plane: PlaneDto) -> UUID:
        async with new_session() as session:
            data = plane.model_dump()
            if data['current_fuel'] > data['fuel_consumption'] * data['max_distance']:
                raise ValueError('Current fuel must be less than or equal to (max distance * fuel consumption)')
            query = select(PlaneSchema).filter_by(model=data['model'])
            result = await session.execute(query)
            existing_plane = result.scalar_one_or_none()
            if existing_plane is not None:
                raise ValueError('Plane already exists')
            new_plane = PlaneSchema(**data)
            new_plane.id = uuid4()
            session.add(new_plane)
            await session.flush()
            await session.commit()
            return new_plane.id

    @classmethod
    async def edit_plane(cls, plane_id: UUID, plane: PlaneDto) -> Plane:
        async with (new_session() as session):
            data = plane.model_dump()
            query = select(PlaneSchema).filter_by(id=plane_id)
            result = await session.execute(query)
            plane_to_change = result.scalar_one()
            for key, value in data.items():
                setattr(plane_to_change, key, value)
            await session.commit()
            return Plane.from_orm(plane_to_change)

    @classmethod
    async def delete_plane(cls, plane_id: UUID) -> Plane:
        async with (new_session() as session):
            query = select(PlaneSchema).filter_by(id=plane_id)
            result = await session.execute(query)
            plane_to_delete = result.scalar_one()
            await session.delete(plane_to_delete)
            await session.commit()
            return Plane.from_orm(plane_to_delete)

    @classmethod
    async def get_planes(cls) -> list[Plane]:
        async with new_session() as session:
            query = select(PlaneSchema)
            result = await session.execute(query)
            plane_models = result.scalars().all()
            return [Plane.from_orm(x) for x in plane_models]

    @classmethod
    async def get_average_capacity(cls) -> int:
        async with new_session() as session:
            query = select(PlaneSchema.max_capacity)
            result = await session.execute(query)
            plane_capacities = [int(x) for x in result.scalars().all()]
            if len(plane_capacities) == 0:
                raise ZeroDivisionError('No planes available')
            average = sum(plane_capacities) / len(plane_capacities)
            return round(average)

    @classmethod
    async def get_average_distance(cls) -> int:
        async with new_session() as session:
            query = select(PlaneSchema.max_distance)
            result = await session.execute(query)
            plane_distances = [int(x) for x in result.scalars().all()]
            if len(plane_distances) == 0:
                raise ZeroDivisionError('No planes available')
            average = sum(plane_distances) / len(plane_distances)
            return round(average)

    @classmethod
    async def get_max_capacity(cls) -> int:
        async with new_session() as session:
            query = select(PlaneSchema.max_capacity)
            result = await session.execute(query)
            plane_capacities = [int(x) for x in result.scalars().all()]
            if len(plane_capacities) == 0:
                raise ValueError('No planes available')
            max_capacity = max(plane_capacities)
            return max_capacity

    @classmethod
    async def get_max_distance(cls) -> int:
        async with new_session() as session:
            query = select(PlaneSchema.max_distance)
            result = await session.execute(query)
            plane_distances = [int(x) for x in result.scalars().all()]
            if len(plane_distances) == 0:
                raise ValueError('No planes available')
            max_distance = max(plane_distances)
            return max_distance
