from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


class PlaneDto(BaseModel):
    model: str
    max_capacity: int
    max_distance: int
    current_fuel: int
    fuel_consumption: int

    @field_validator('max_capacity')
    def check_capacity(cls, inpt: int) -> int:
        if inpt <= 0:
            raise ValueError('Capacity must be a positive integer')
        return inpt

    @field_validator('max_distance')
    def check_distance(cls, inpt: int) -> int:
        if inpt <= 0:
            raise ValueError('Distance must be a positive integer')
        return inpt

    @field_validator('current_fuel')
    def check_current_fuel(cls, field_value: int) -> int:
        if field_value < 0:
            raise ValueError('Current fuel must be non-negative')
        return field_value

    @field_validator('fuel_consumption')
    def check_fuel_consumption(cls, cons: int) -> int:
        if cons <= 0:
            raise ValueError('Fuel consumption must be a positive integer')
        return cons


class Plane(BaseModel):
    id: UUID
    model: str
    max_capacity: int
    max_distance: int
    current_fuel: int
    fuel_consumption: int
    model_config = ConfigDict(from_attributes=True)
