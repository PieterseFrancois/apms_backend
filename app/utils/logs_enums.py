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
    Each value corresponds to the new ENUM type used in the database.
    """

    ERROR_HEAT = "ERROR_HEAT"
    ERROR_FAN = "ERROR_FAN"
    BAKE_SAFE = "BAKE_SAFE"
    BAKE_UNSAFE = "BAKE_UNSAFE"
    OVERRIDE_SAFETY = "OVERRIDE_SAFETY"
    PHASE_IDLE = "PHASE_IDLE"
    PHASE_HEATING = "PHASE_HEATING"
    PHASE_BAKING = "PHASE_BAKING"
    PHASE_COOLING = "PHASE_COOLING"
    PHASE_FINISHED = "PHASE_FINISHED"
    BAKE_BATCH = "BAKE_BATCH"
    STOP_BAKE = "STOP_BAKE"

    def __str__(self) -> str:
        return self.value

    @property
    def category(self):
        """Maps the enum to its corresponding category."""
        mapping = {
            OvenLogType.ERROR_HEAT: LogType.ERROR,
            OvenLogType.ERROR_FAN: LogType.ERROR,
            OvenLogType.BAKE_SAFE: LogType.SAFETY,
            OvenLogType.BAKE_UNSAFE: LogType.SAFETY,
            OvenLogType.OVERRIDE_SAFETY: LogType.COMMAND,
            OvenLogType.PHASE_IDLE: LogType.PHASE,
            OvenLogType.PHASE_HEATING: LogType.PHASE,
            OvenLogType.PHASE_BAKING: LogType.PHASE,
            OvenLogType.PHASE_COOLING: LogType.PHASE,
            OvenLogType.PHASE_FINISHED: LogType.PHASE,
            OvenLogType.BAKE_BATCH: LogType.COMMAND,
            OvenLogType.STOP_BAKE: LogType.COMMAND,
        }
        return mapping[self]

    @property
    def description(self):
        """Maps the enum to its corresponding description."""
        mapping = {
            OvenLogType.ERROR_HEAT: OvenLogDescription.ERROR_HEAT,
            OvenLogType.ERROR_FAN: OvenLogDescription.ERROR_FAN,
            OvenLogType.BAKE_SAFE: OvenLogDescription.BAKE_SAFE,
            OvenLogType.BAKE_UNSAFE: OvenLogDescription.BAKE_UNSAFE,
            OvenLogType.OVERRIDE_SAFETY: OvenLogDescription.OVERRIDE_SAFETY,
            OvenLogType.PHASE_IDLE: OvenLogDescription.PHASE_IDLE,
            OvenLogType.PHASE_HEATING: OvenLogDescription.PHASE_HEATING,
            OvenLogType.PHASE_BAKING: OvenLogDescription.PHASE_BAKING,
            OvenLogType.PHASE_COOLING: OvenLogDescription.PHASE_COOLING,
            OvenLogType.PHASE_FINISHED: OvenLogDescription.PHASE_FINISHED,
            OvenLogType.BAKE_BATCH: OvenLogDescription.BAKE_BATCH,
            OvenLogType.STOP_BAKE: OvenLogDescription.STOP_BAKE,
        }
        return mapping[self]


class PressLogType(Enum):
    """
    Represents the different types of logs for the press.
    Each value corresponds to the new ENUM type used in the database.
    """

    ERROR_PRESS = "ERROR_PRESS"
    ERROR_LOAD = "ERROR_LOAD"
    PRESS_SAFE = "PRESS_SAFE"
    PRESS_UNSAFE = "PRESS_UNSAFE"
    OVERRIDE_SAFETY = "OVERRIDE_SAFETY"
    PHASE_IDLE = "PHASE_IDLE"
    PHASE_INSERTING = "PHASE_INSERTING"
    PHASE_LOADING = "PHASE_LOADING"
    PHASE_PRESSING = "PHASE_PRESSING"
    PHASE_EXTRACTING = "PHASE_EXTRACTING"
    PHASE_FINISHED = "PHASE_FINISHED"
    CONFIRM_INSERTION = "CONFIRM_INSERTION"
    PRESS_BATCH = "PRESS_BATCH"
    STOP_PRESS = "STOP_PRESS"
    OPEN_PRESS = "OPEN_PRESS"

    def __str__(self) -> str:
        return self.value

    @property
    def category(self):
        """Maps the enum to its corresponding category."""
        mapping = {
            PressLogType.ERROR_PRESS: LogType.ERROR,
            PressLogType.ERROR_LOAD: LogType.ERROR,
            PressLogType.PRESS_SAFE: LogType.SAFETY,
            PressLogType.PRESS_UNSAFE: LogType.SAFETY,
            PressLogType.OVERRIDE_SAFETY: LogType.COMMAND,
            PressLogType.PHASE_IDLE: LogType.PHASE,
            PressLogType.PHASE_INSERTING: LogType.PHASE,
            PressLogType.PHASE_LOADING: LogType.PHASE,
            PressLogType.PHASE_PRESSING: LogType.PHASE,
            PressLogType.PHASE_EXTRACTING: LogType.PHASE,
            PressLogType.PHASE_FINISHED: LogType.PHASE,
            PressLogType.CONFIRM_INSERTION: LogType.CONFIRMATION,
            PressLogType.PRESS_BATCH: LogType.COMMAND,
            PressLogType.STOP_PRESS: LogType.COMMAND,
            PressLogType.OPEN_PRESS: LogType.COMMAND,
        }
        return mapping[self]

    @property
    def description(self):
        """Maps the enum to its corresponding description."""
        mapping = {
            PressLogType.ERROR_PRESS: PressLogDescription.ERROR_PRESS,
            PressLogType.ERROR_LOAD: PressLogDescription.ERROR_LOAD,
            PressLogType.PRESS_SAFE: PressLogDescription.PRESS_SAFE,
            PressLogType.PRESS_UNSAFE: PressLogDescription.PRESS_UNSAFE,
            PressLogType.OVERRIDE_SAFETY: PressLogDescription.OVERRIDE_SAFETY,
            PressLogType.PHASE_IDLE: PressLogDescription.PHASE_IDLE,
            PressLogType.PHASE_INSERTING: PressLogDescription.PHASE_INSERTING,
            PressLogType.PHASE_LOADING: PressLogDescription.PHASE_LOADING,
            PressLogType.PHASE_PRESSING: PressLogDescription.PHASE_PRESSING,
            PressLogType.PHASE_EXTRACTING: PressLogDescription.PHASE_EXTRACTING,
            PressLogType.PHASE_FINISHED: PressLogDescription.PHASE_FINISHED,
            PressLogType.CONFIRM_INSERTION: PressLogDescription.CONFIRM_INSERTION,
            PressLogType.PRESS_BATCH: PressLogDescription.PRESS_BATCH,
            PressLogType.STOP_PRESS: PressLogDescription.STOP_PRESS,
            PressLogType.OPEN_PRESS: PressLogDescription.OPEN_PRESS,
        }
        return mapping[self]
