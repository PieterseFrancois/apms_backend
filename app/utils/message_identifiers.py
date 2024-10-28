from enum import Enum


class MessageIdentifiers(Enum):
    """
    Represents the message identifiers associated with the MQTT and websocket messages.
    """

    # Oven
    BakeBatch = "BakeBatch"
    StopBake = "StopBake"
    EHeat = "EHeat"
    EFan = "EFan"
    BakeSafe = "BakeSafe"
    BakeOverride = "BakeOverride"
    SafeTemp = "SafeTemp"
    DesiredTemp = "DesiredTemp"
    MaxTemp = "MaxTemp"
    BakeTime = "BakeTime"
    Humidity = "Humidity"
    CurrentTemp = "CurrentTemp"
    BakePhase = "BakePhase"
    OvenLog = "OvenLog"
    ActiveProfile = "ActiveProfile"

    # Press
    Pressbatch = "Pressbatch"
    StopPress = "StopPress"
    OpenPress = "OpenPress"
    ConfirmInserted = "ConfIns"
    EPress = "EPress"
    ELoad = "ELoad"
    PressSafe = "PressSafe"
    PressOverride = "PressOverride"
    CurrentDistance = "CurrentDist"
    PressPhase = "PressPhase"
    PressLog = "PressLog"

    def __str__(self) -> str:
        return self.value
