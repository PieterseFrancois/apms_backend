from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages
from app.utils.message_identifiers import MessageIdentifiers

from app.schemas import (
    Response,
    TemperatureLogBase,
)

from app.crud.oven import (
    create_temperature_log,
    get_temperature_logs,
)

from datetime import datetime, timezone
import os

from app.websocket import manager as WebSocketManager
import json

router = APIRouter()


@router.post("/oven/log/temperature", response_model=Response, tags=["Oven"])
async def create_temperature_log_route(
    temperature: float,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a temperature log for the oven.

    Parameters:
    - temperature (float): The temperature value.
    - db (Session): The database session.

    Returns:
    - Response: The response containing the log details.
    """

    result = create_temperature_log(db, temperature)

    temperature_log = TemperatureLogBase(
        temperature=result.temperature,
        created_at=result.created_at,
    )

    # Broadcast the temperature log to all connected clients.
    await WebSocketManager.broadcast(
        temperature_log.dict(), MessageIdentifiers.CurrentTemp
    )

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_LOG_CREATED,
        data=[temperature_log],
    )


@router.get("/oven/logs/temperature", response_model=Response, tags=["Oven"])
def get_temperature_logs_route(
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves all the temperature logs.

    Parameters:
    - db (Session): The database session.

    Returns:
    - Response: The response containing the list of temperature logs.
    """

    temperature_logs: list[TemperatureLogBase] = get_temperature_logs(db)

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_LOGS_RETRIEVED,
        data=temperature_logs,
    )


@router.get("/oven/start", response_model=Response, tags=["Oven"])
def start_oven() -> Response:
    """
    Starts the oven.

    Returns:
    - Response: The response containing the oven status.
    """

    # Publish a message to the oven's MQTT topic to start the oven.
    # This is a placeholder for the actual implementation.

    # Temporarily create a text file logging the time and command.
    current_time = datetime.now(tz=timezone.utc)
    print(f"Oven started at {current_time}.")

    return Response(success=True, msg=HTTPMessages.OVEN_STARTED, data=[])


@router.get("/oven/stop", response_model=Response, tags=["Oven"])
def stop_oven() -> Response:
    """
    Stops the oven.

    Returns:
    - Response: The response containing the oven status.
    """

    # Publish a message to the oven's MQTT topic to stop the oven.
    # This is a placeholder for the actual implementation.

    # Temporarily create a text file logging the time and command.
    current_time = datetime.now(tz=timezone.utc)
    print(f"Oven stopped at {current_time}.")

    return Response(success=True, msg=HTTPMessages.OVEN_STOPPED, data=[])
