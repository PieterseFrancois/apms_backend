from pydantic import BaseModel

from datetime import datetime


class TemperatureLogBase(BaseModel):
    """
    Represents the temperature logs schema.

    Attributes:
        temperature (float): The temperature value.
        created_at (datetime): The timestamp when the log was created
        machine_id (int): The machine ID.
        batch_id (int | None): The batch ID

    """

    temperature: float
    created_at: datetime
    machine_id: int
    batch_id: int | None

    class Config:
        from_attributes = True


class TemperatureLogCreate(BaseModel):
    """
    Represents the temperature logs schema for creation.

    Attributes:
        temperature (float): The temperature value.
        machine_id (int): The machine ID.
        batch_id (int | None): The batch ID.

    """

    temperature: float
    machine_id: int
    batch_id: int | None


class TemperatureLog(TemperatureLogBase):
    """
    Represents the temperature logs schema for response.

    Attributes:
        id (int): The primary key of the table.
        temperature (float): The temperature value.
        created_at (datetime): The timestamp when the log was created
        machine_id (int): The machine ID.
        batch_id (int): The batch ID.

    """

    id: int

    class Config:
        from_attributes = True
