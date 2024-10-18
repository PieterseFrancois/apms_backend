from typing import Union
from pydantic import BaseModel
from app.utils.http_messages import HTTPMessages

from app.schemas.machine import (
    Machine,
    MachineBase,
    MachineCreate,
    MachineUpdate,
)
from app.schemas.oven_batch import (
    OvenBatchBase,
    OvenBatchCreate,
    OvenBatch,
)
from app.schemas.temperature_log import (
    TemperatureLogBase,
    TemperatureLogCreate,
    TemperatureLog,
)
from app.schemas.oven_logs import (
    OvenLogBase,
    OvenLogCreate,
    OvenLog,
    OvenLogExpanded,
)


class Response(BaseModel):
    """
    Represents the response data for an API request.

    Attributes:
        success (bool): Indicates the success status of the API response.
        msg (HTTPMessages): The HTTP message associated with the API response.
        data (Union[
            list[],
        ]): The list of data returned by the API response.

    """

    success: bool
    msg: HTTPMessages
    data: Union[
        list[Machine],
        list[MachineBase],
        list[MachineCreate],
        list[MachineUpdate],
        list[OvenBatchBase],
        list[OvenBatchCreate],
        list[OvenBatch],
        list[TemperatureLogBase],
        list[TemperatureLogCreate],
        list[TemperatureLog],
        list[OvenLogBase],
        list[OvenLogCreate],
        list[OvenLog],
        list[OvenLogExpanded],
        None,
        list[None],
    ]
