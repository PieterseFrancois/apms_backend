from enum import Enum


class MessageIdentifiers(Enum):
    """
    Represents the message identifiers associated with the MQTT and websocket messages.
    """

    # Oven
    RequestStartOven = "RequestStartOven"
    RequestStopOven = "RequestStopOven"
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
    RequestStartPress = "RequestStartPress"
    RequestStopPress = "RequestStopPress"
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

    # Machine
    MachineConnected = "MachineConnected"
    MachineDisconnected = "MachineDisconnected"

    def __str__(self) -> str:
        return self.value
