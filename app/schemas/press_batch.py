from pydantic import BaseModel

from datetime import datetime
from app.utils.state_enum import BatchState


class PressBatchBase(BaseModel):
    """
    Represents the base schema for the press batches.

    Attributes:
        start_time (datetime): The start time of the batch.
        state (BatchState): The state of the batch.
        machine_id (int): The machine identifier.
    """

    start_time: datetime
    state: BatchState
    machine_id: int


class PressBatchCreate(PressBatchBase):
    """
    Represents the schema for creating an press batch.

    Inherits:
        PressBatchBase
    """

    pass


class PressBatch(PressBatchBase):
    """
    Represents the schema for the press batches.

    Attributes:
        id (int): The identifier of the batch.
        stop_time (datetime): The stop time of the batch.

    Inherits:
        PressBatchBase
    """

    id: int
    stop_time: datetime | None

    class Config:
        from_attributes = True
