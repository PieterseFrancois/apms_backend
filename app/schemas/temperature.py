from pydantic import BaseModel

from datetime import datetime


class TemperatureLogBase(BaseModel):
    """
    Represents the base schema for the temperature logs.

    Attributes:
        temperature (float): The temperature value.
        created_at (datetime): The timestamp when the log was created.
    """

    temperature: float
    created_at: datetime

    class Config:
        from_attributes = True
