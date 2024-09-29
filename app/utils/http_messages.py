from enum import Enum


class HTTPMessages(Enum):
    """
    Represents the HTTP messages associated with an API response.
    """

    VALIDATION_ERROR = "Validation error."
    DATA_INTEGRITY_ERROR = "Data integrity error."
    INTERNAL_SERVER_ERROR = "Internal server error."
    TEMPERATURE_LOG_CREATED = "Temperature log created successfully."
    TEMPERATURE_LOGS_RETRIEVED = "Temperature logs retrieved successfully."
    OVEN_STARTED = "Oven started successfully."
    OVEN_STOPPED = "Oven stopped successfully."

    def __str__(self) -> str:
        return self.value
