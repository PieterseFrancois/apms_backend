from enum import Enum


class LogType(Enum):
    """
    Represents the different types of logs.
    """

    ERROR = "Error"
    SAFETY = "Safety"
    COMMAND = "Command"
    PHASE = "Phase"
    CONFIRMATION = "Confirmation"

    def __str__(self) -> str:
        return self.value


class OvenLogDescription(Enum):
    """
    Represents the different descriptions for the oven logs.
    """

    ERROR_HEAT = "Error in heating process."
    ERROR_FAN = "Error in fan operation."
    BAKE_SAFE = "Baking process safety check passed."
    BAKE_UNSAFE = "Baking process safety check failed."
    OVERRIDE_SAFETY = "Safety check overridden."
    PHASE_IDLE = "Oven is idle."
    PHASE_HEATING = "Oven is heating up."
    PHASE_BAKING = "Oven is baking."
    PHASE_COOLING = "Oven is cooling down."
    PHASE_FINISHED = "Baking process finished."
    BAKE_BATCH = "Starting oven to bake a batch."
    STOP_BAKE = "Stopping oven and baking process."

    def __str__(self) -> str:
        return self.value


class PressLogDescription(Enum):
    """
    Represents the different descriptions for the press logs.
    """

    ERROR_PRESS = "Error in press operation."
    ERROR_LOAD = "Error in loading process."
    PRESS_SAFE = "Press process safety check passed."
    PRESS_UNSAFE = "Press process safety check failed."
    OVERRIDE_SAFETY = "Safety check overridden."
    PHASE_IDLE = "Press is idle."
    PHASE_INSERTING = "Pulp is being inserted into press."
    PHASE_LOADING = "Press is loading form."
    PHASE_PRESSING = "Press is pressing."
    PHASE_EXTRACTING = "Press is extracting finished form."
    PHASE_FINISHED = "Press process finished."
    CONFIRM_INSERTION = "Confirmed pulp inserted into press."
    PRESS_BATCH = "Starting press to form a pot."
    STOP_PRESS = "Stopping press and pressing process."
    OPEN_PRESS = "Opening press."

    def __str__(self) -> str:
        return self.value


class OvenLogType(Enum):
    """
    Represents the different types of logs for the oven.
    Each log type has a category and a description associated with it.
    """

    ERROR_HEAT = (LogType.ERROR, OvenLogDescription.ERROR_HEAT)
    ERROR_FAN = (LogType.ERROR, OvenLogDescription.ERROR_FAN)
    BAKE_SAFE = (LogType.SAFETY, OvenLogDescription.BAKE_SAFE)
    BAKE_UNSAFE = (LogType.SAFETY, OvenLogDescription.BAKE_UNSAFE)
    OVERRIDE_SAFETY = (LogType.COMMAND, OvenLogDescription.OVERRIDE_SAFETY)
    PHASE_IDLE = (LogType.PHASE, OvenLogDescription.PHASE_IDLE)
    PHASE_HEATING = (LogType.PHASE, OvenLogDescription.PHASE_HEATING)
    PHASE_BAKING = (LogType.PHASE, OvenLogDescription.PHASE_BAKING)
    PHASE_COOLING = (LogType.PHASE, OvenLogDescription.PHASE_COOLING)
    PHASE_FINISHED = (LogType.PHASE, OvenLogDescription.PHASE_FINISHED)
    BAKE_BATCH = (LogType.COMMAND, OvenLogDescription.BAKE_BATCH)
    STOP_BAKE = (LogType.COMMAND, OvenLogDescription.STOP_BAKE)

    def __init__(self, category, description):
        self.category = category
        self.description = description


class PressLogType(Enum):
    """
    Represents the different types of logs for the press.
    Each log type has a category and a description associated with it.
    """

    ERROR_PRESS = (LogType.ERROR, PressLogDescription.ERROR_PRESS)
    ERROR_LOAD = (LogType.ERROR, PressLogDescription.ERROR_LOAD)
    PRESS_SAFE = (LogType.SAFETY, PressLogDescription.PRESS_SAFE)
    PRESS_UNSAFE = (LogType.SAFETY, PressLogDescription.PRESS_UNSAFE)
    OVERRIDE_SAFETY = (LogType.COMMAND, PressLogDescription.OVERRIDE_SAFETY)
    PHASE_IDLE = (LogType.PHASE, PressLogDescription.PHASE_IDLE)
    PHASE_INSERTING = (LogType.PHASE, PressLogDescription.PHASE_INSERTING)
    PHASE_LOADING = (LogType.PHASE, PressLogDescription.PHASE_LOADING)
    PHASE_PRESSING = (LogType.PHASE, PressLogDescription.PHASE_PRESSING)
    PHASE_EXTRACTING = (LogType.PHASE, PressLogDescription.PHASE_EXTRACTING)
    PHASE_FINISHED = (LogType.PHASE, PressLogDescription.PHASE_FINISHED)
    CONFIRM_INSERTION = (LogType.CONFIRMATION, PressLogDescription.CONFIRM_INSERTION)
    PRESS_BATCH = (LogType.COMMAND, PressLogDescription.PRESS_BATCH)
    STOP_PRESS = (LogType.COMMAND, PressLogDescription.STOP_PRESS)
    OPEN_PRESS = (LogType.COMMAND, PressLogDescription.OPEN_PRESS)

    def __init__(self, category, description):
        self.category = category
        self.description = description
