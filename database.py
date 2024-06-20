from uuid import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Table, ForeignKey


engine = create_async_engine("sqlite+aiosqlite:///planes.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("flight_id", ForeignKey("flights.id")),
    Column("plane_id", ForeignKey("planes.id")),
)


class PlaneSchema(Base):
    __tablename__ = "planes"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    model: Mapped[str]
    max_capacity: Mapped[int]
    max_distance: Mapped[int]
    current_fuel: Mapped[int]
    fuel_consumption: Mapped[int]


class FlightSchema(Base):
    __tablename__ = "flights"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    begin_airport: Mapped[str]
    end_airport: Mapped[str]
    distance: Mapped[int]
    passengers: Mapped[int]
    suitable_planes: Mapped[list[PlaneSchema]] = relationship(secondary=association_table)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
