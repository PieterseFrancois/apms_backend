from pydantic import BaseModel
from datetime import datetime

from app.utils.logs_enums import LogType, OvenLogDescription, OvenLogType


class OvenLogBase(BaseModel):
    """
    Represents the base schema for the oven logs.

    Attributes:
        machine_id (int): The ID of the machine.
        type (LogType): The type of log.
        description (OvenLogDescription): The description of the log.
    """

    machine_id: int
    type: OvenLogType


class OvenLogCreate(BaseModel):
    """
    Represents the schema for creating an oven log.

    Attributes:
        machine_id (int): The ID of the machine.
        type (OvenLogType): The type of log.
        batch_id (int | None): The batch
    """

    machine_id: int
    type: OvenLogType
    batch_id: int | None


class OvenLog(OvenLogBase):
    """
    Represents the schema for the oven logs.

    Attributes:
        id (int): The primary key of the table.
        batch_id (int | None): The batch
        created_at (datetime): The timestamp when the log was created.
        machine_id (int): The ID of the machine.
        type (OvenLogType): The type of log.

    Inherits:
        OvenLogBase
    """

    id: int
    batch_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class OvenLogExpanded(BaseModel):
    """
    Represents the schema for the oven logs with expanded data.

    Attributes:
        id (int): The primary key of the table.
        created_at (datetime): The timestamp when the log was created.
        machine_id (int): The ID of the machine.
        type (LogType): The type of log.
        description (OvenLogDescription): The description of the log.
        batch_id (int | None): The batch

    """

    id: int
    batch_id: int | None
    created_at: datetime
    machine_id: int
    type: LogType
    description: OvenLogDescription

    class Config:
        from_attributes = True
