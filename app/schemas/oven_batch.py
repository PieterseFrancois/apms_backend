from pydantic import BaseModel

from datetime import datetime
from app.utils.state_enum import BatchState


class OvenBatchBase(BaseModel):
    """
    Represents the base schema for the oven batches.

    Attributes:
        start_time (datetime): The start time of the batch.
        state (BatchState): The state of the batch.
        machine_id (int): The machine identifier.
    """

    start_time: datetime
    state: BatchState
    machine_id: int


class OvenBatchCreate(OvenBatchBase):
    """
    Represents the schema for creating an oven batch.

    Inherits:
        OvenBatchBase
    """

    pass


class OvenBatch(OvenBatchBase):
    """
    Represents the schema for the oven batches.

    Attributes:
        id (int): The identifier of the batch.
        stop_time (datetime): The stop time of the batch.

    Inherits:
        OvenBatchBase
    """

    id: int
    stop_time: datetime | None

    class Config:
        from_attributes = True
