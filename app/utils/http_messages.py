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
    # Websocket
    WEBSOCKET_FAILURE_OVEN_COMMAND = (
        "Failed to send the oven command over the websocket."
    )

    # Oven
    OVEN_STARTED = "Oven started successfully."
    OVEN_STOPPED = "Oven stopped successfully."
    OVEN_START_FAILED = "Failed to start the oven."
    OVEN_STOP_FAILED = "Failed to stop the oven."
    OVEN_STATUS_RETRIEVED = "Oven status retrieved successfully."
    OVEN_LOG_CREATED = "Oven log created successfully."
    OVEN_LOGS_RETRIEVED = "Oven logs retrieved successfully."

    # Machines
    MACHINE_CREATED = "Machine created successfully."
    MACHINE_RETRIEVED = "Machine retrieved successfully."
    MACHINES_RETRIEVED = "Machines retrieved successfully."
    MACHINE_UPDATED = "Machine updated successfully."
    MACHINE_DELETED = "Machine deleted successfully."

    def __str__(self) -> str:
        return self.value
