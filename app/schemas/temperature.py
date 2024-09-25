from pydantic import BaseModel

from datetime import datetime


class TemperatureLogBase(BaseModel):
    """
    Represents the base schema for the temperature logs.

    Attributes:
        temperature (float): The temperature value.
        time (datetime): The timestamp when the log was created.
    """

    temperature: float
    time: datetime
