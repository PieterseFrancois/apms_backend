from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.websocket import manager as WebSocketManager
from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages
from app.utils.message_identifiers import MessageIdentifiers
from app.utils.state_enum import BatchState

from app.schemas import (
    Response,
    OvenBatchCreate,
    OvenBatch,
    TemperatureLogBase,
)

from app.crud.oven import (
    create_oven_batch,
    get_latest_oven_batch_for_machine,
    stop_active_oven_batch,
    create_temperature_log,
    get_temperature_logs,
)

from datetime import datetime, timezone

router = APIRouter()


@router.get("/oven/start/{machine_id}", response_model=Response, tags=["Oven"])
async def start_oven(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Starts the oven.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the oven status.
    """

    # Create oven batch
    new_oven_batch = OvenBatchCreate(
        start_time=datetime.now(tz=timezone.utc),
        state=BatchState.ACTIVE,
        machine_id=machine_id,
    )

    oven_batch: OvenBatchCreate = create_oven_batch(db, new_oven_batch)

    # MQTT
    try:
        print("MQTT message sent to start oven.")
        # Publish a message to the oven's MQTT topic to start the oven.
        # This is a placeholder for the actual implementation.
    except Exception as e:
        # Create log entry
        # Placeholder for the actual implementation.

        stop_active_oven_batch(db, machine_id)

        return Response(success=False, msg=HTTPMessages.OVEN_START_FAILED, data=[])

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.BakeBatch
        )
    except Exception as e:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_OVEN_COMMAND, data=[]
        )

    # Create log entry
    # Placeholder for the actual implementation.

    return Response(success=True, msg=HTTPMessages.OVEN_STARTED, data=[oven_batch])


@router.get("/oven/stop/{machine_id}", response_model=Response, tags=["Oven"])
async def stop_oven(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Stops the oven.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the oven status.
    """

    # MQTT
    try:
        print("MQTT message sent to stop oven.")
        # Publish a message to the oven's MQTT topic to stop the oven.
        # This is a placeholder for the actual implementation.
    except Exception as e:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(success=False, msg=HTTPMessages.OVEN_STOP_FAILED, data=[])

    # Stop the active oven batch
    stop_active_oven_batch(db, machine_id)

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.StopBake
        )
    except Exception as e:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_OVEN_COMMAND, data=[]
        )

    # Create log entry
    # Placeholder for the actual implementation.

    return Response(success=True, msg=HTTPMessages.OVEN_STOPPED, data=[])


@router.get("/oven/status/{machine_id}", response_model=Response, tags=["Oven"])
def get_oven_status_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the oven status.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the oven status.
    """

    oven_batch: OvenBatch = get_latest_oven_batch_for_machine(db, machine_id)

    return Response(
        success=True, msg=HTTPMessages.OVEN_STATUS_RETRIEVED, data=[oven_batch]
    )


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
