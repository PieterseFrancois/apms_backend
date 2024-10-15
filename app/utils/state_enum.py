from enum import Enum


class BatchState(Enum):
    """
    Represents the different states of a batch.
    """

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return self.value
