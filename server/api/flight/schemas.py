from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from server.api.plane.schemas import Plane


class FlightDto(BaseModel):
    begin_airport: str
    end_airport: str
    distance: int
    passengers: int

    @field_validator('distance')
    def check_distance(cls, inpt: int) -> int:
        if inpt <= 0:
            raise ValueError('Distance must be a positive integer')
        return inpt

    @field_validator('passengers')
    def check_passengers(cls, inpt: int) -> int:
        if inpt <= 0:
            raise ValueError('Passengers must be a positive integer')
        return inpt


class Flight(BaseModel):
    id: UUID
    begin_airport: str
    end_airport: str
    distance: int
    passengers: int
    suitable_planes: list[Plane] | None = None
    model_config = ConfigDict(from_attributes=True)
