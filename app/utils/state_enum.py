from enum import Enum


class BatchState(Enum):
    """
    Represents the different states of a batch.
    """

    ACTIVE = "Active"
    COMPLETED = "Completed"
    ERROR = "Error"
