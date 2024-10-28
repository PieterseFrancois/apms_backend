from pydantic import BaseModel
from datetime import datetime

from app.utils.logs_enums import LogType, PressLogDescription, PressLogType


class PressLogBase(BaseModel):
    """
    Represents the base schema for the press logs.

    Attributes:
        machine_id (int): The ID of the machine.
        type (LogType): The type of log.
    """

    machine_id: int
    type: PressLogType


class PressLogCreate(BaseModel):
    """
    Represents the schema for creating an press log.

    Attributes:
        machine_id (int): The ID of the machine.
        type (PressLogType): The type of log.
        batch_id (int | None): The batch
    """

    machine_id: int
    type: PressLogType
    batch_id: int | None


class PressLog(PressLogBase):
    """
    Represents the schema for the press logs.

    Attributes:
        id (int): The primary key of the table.
        batch_id (int | None): The batch
        created_at (datetime): The timestamp when the log was created.
        machine_id (int): The ID of the machine.
        type (PressLogType): The type of log.

    Inherits:
        PressLogBase
    """

    id: int
    batch_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class PressLogExpanded(BaseModel):
    """
    Represents the schema for the press logs with expanded data.

    Attributes:
        id (int): The primary key of the table.
        created_at (datetime): The timestamp when the log was created.
        machine_id (int): The ID of the machine.
        type (LogType): The type of log.
        description (PressLogDescription): The description of the log.
        batch_id (int | None): The batch

    """

    id: int
    batch_id: int | None
    created_at: datetime
    machine_id: int
    type: LogType
    description: PressLogDescription

    class Config:
        from_attributes = True
