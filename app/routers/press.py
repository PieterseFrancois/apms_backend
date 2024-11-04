from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.websocket import manager as WebSocketManager
from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages
from app.utils.message_identifiers import MessageIdentifiers
from app.utils.logs_enums import PressLogType

from app.schemas import (
    Response,
    PressBatchCreate,
    PressBatch,
    PressLogCreate,
    PressLog,
    PressLogExpanded,
)

from app.crud.press import (
    create_press_batch,
    get_latest_press_batch_for_machine,
    get_press_batches_for_machine,
    stop_active_press_batch,
    create_log,
    get_logs_for_machine,
)

from app.utils.state_enum import BatchState

from datetime import datetime, timezone

router = APIRouter()

GROUP_1_ID: int = 8


@router.get("/press/request_start/{machine_id}", response_model=Response, tags=["Press"])
async def request_start_press(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Requests to start the press.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press status.
    """

    # Send a message to the HMI to start the press
    await WebSocketManager.send_personal_message(
        "", machine_id, MessageIdentifiers.RequestStartPress
    )

    # Bypass group for demonstration purposes
    if (machine_id == GROUP_1_ID):
        await start_press(machine_id, db)

    return Response(success=True, msg=HTTPMessages.PRESS_START_REQUEST, data=[]) 


@router.get("/press/request_stop/{machine_id}", response_model=Response, tags=["Press"])
async def request_stop_press(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Requests to stop the press.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press status.
    """

    # Send a message to the HMI to stop the press
    await WebSocketManager.send_personal_message(
        "", machine_id, MessageIdentifiers.RequestStopPress
    )

    # Bypass group for demonstration purposes
    if (machine_id == GROUP_1_ID):
        await stop_press(machine_id, db)

    return Response(success=True, msg=HTTPMessages.PRESS_STOP_REQUEST, data=[])


@router.get("/press/start/{machine_id}", response_model=Response, tags=["Press"])
async def start_press(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Starts the press.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press status.
    """
    stop_active_press_batch(db, machine_id)

    # Create press batch
    new_press_batch = PressBatchCreate(
        start_time=datetime.now(tz=timezone.utc),
        state=BatchState.ACTIVE,
        machine_id=machine_id,
    )
    press_batch: PressBatchCreate = create_press_batch(db, new_press_batch)

    # MQTT
    try:
        print("MQTT message sent to start press.")
        # Publish a message to the press's MQTT topic to start the press.
        # This is a placeholder for the actual implementation.
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        stop_active_press_batch(db, machine_id)

        return Response(success=False, msg=HTTPMessages.PRESS_START_FAILED, data=[])

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.Pressbatch
        )
    except Exception:
        # Create log entry
        # create_log_route(machine_id, PressLogType.ERROR, None, db)

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_PRESS_COMMAND, data=[]
        )

    # Create log entry
    await create_log_route(machine_id, PressLogType.PRESS_BATCH, None, db)

    return Response(success=True, msg=HTTPMessages.PRESS_STARTED, data=[press_batch])


@router.get("/press/stop/{machine_id}", response_model=Response, tags=["Press"])
async def stop_press(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Stops the press.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press status.
    """

    # MQTT
    try:
        print("MQTT message sent to stop press.")
        # Publish a message to the press's MQTT topic to stop the press.
        # This is a placeholder for the actual implementation.
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(success=False, msg=HTTPMessages.PRESS_STOP_FAILED, data=[])

    # Stop the active press batch
    stop_active_press_batch(db, machine_id)

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.StopPress
        )
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_PRESS_COMMAND, data=[]
        )

    # Create log entry
    await create_log_route(machine_id, PressLogType.STOP_PRESS, None, db)

    return Response(success=True, msg=HTTPMessages.PRESS_STOPPED, data=[])


@router.get("/press/status/{machine_id}", response_model=Response, tags=["Press"])
def get_press_status_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the press status.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press status.
    """

    press_batch: PressBatch | None = get_latest_press_batch_for_machine(db, machine_id)

    return Response(
        success=True, msg=HTTPMessages.PRESS_STATUS_RETRIEVED, data=[press_batch]
    )


@router.get("/press/batches/{machine_id}", response_model=Response, tags=["Press"])
def get_press_batches_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the press batches for a machine.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press batches.
    """

    press_batches: list[PressBatch] | None = get_press_batches_for_machine(
        db, machine_id
    )

    return Response(
        success=True, msg=HTTPMessages.PRESS_STATUS_RETRIEVED, data=press_batches
    )


@router.post("/press/log/{machine_id}", response_model=Response, tags=["Press - Log"])
async def create_log_route(
    machine_id: int,
    type: PressLogType,
    batch_id: int | None = None,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a log for the press.

    Args:
        machine_id (int): The machine identifier.
        type (OvenLogType): The type of log.
        batch_id (int | None): The batch identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the log details.
    """

    new_log = PressLogCreate(
        machine_id=machine_id,
        type=type,
        batch_id=batch_id,
    )

    log: PressLog = create_log(db, new_log)

    created_log = PressLogExpanded(
        id=log.id,
        created_at=log.created_at,
        machine_id=log.machine_id,
        type=log.type.category,
        description=log.type.description,
        batch_id=log.batch_id,
    )

    created_log_dict: dict = {
        "id": created_log.id,
        "created_at": created_log.created_at,
        "machine_id": created_log.machine_id,
        "type": created_log.type.value,
        "description": created_log.description.value,
        "batch_id": created_log.batch_id,
    }

    if log.type == PressLogType.PHASE_FINISHED:
        stop_active_press_batch(db, machine_id)

    await WebSocketManager.send_personal_message(
        created_log_dict, machine_id, MessageIdentifiers.PressLog
    )

    return Response(
        success=True, msg=HTTPMessages.PRESS_LOG_CREATED, data=[created_log]
    )


@router.get("/press/logs/{machine_id}", response_model=Response, tags=["Press - Log"])
def get_logs_for_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the logs for the press based on the machine identifier.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the logs.
    """

    logs: list[PressLog] = get_logs_for_machine(db, machine_id)

    expanded_logs = [
        PressLogExpanded(
            id=log.id,
            created_at=log.created_at,
            machine_id=log.machine_id,
            type=log.type.category,
            description=log.type.description,
            batch_id=log.batch_id,
        )
        for log in logs
    ]

    return Response(
        success=True, msg=HTTPMessages.PRESS_LOGS_RETRIEVED, data=expanded_logs
    )


@router.get(
    "/press/confirm_inserted/{machine_id}", response_model=Response, tags=["Press"]
)
async def press_confirm_inserted(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Confirms that the pulp has been inserted into the press.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press confirmation status.
    """

    # MQTT
    try:
        print("MQTT message sent to confirm insert press.")
        # Publish a message to the press's MQTT topic to start the press.
        # This is a placeholder for the actual implementation.
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.
        return Response(
            success=False, msg=HTTPMessages.PRESS_CONFIRMATION_FAILED, data=[]
        )

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.ConfirmInserted
        )
    except Exception:
        # Create log entry
        # create_log_route(machine_id, PressLogType.ERROR, None, db)

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_PRESS_COMMAND, data=[]
        )

    # Create log entry
    await create_log_route(machine_id, PressLogType.CONFIRM_INSERTION, None, db)

    return Response(success=True, msg=HTTPMessages.PRESS_CONFIRM_INSERTED, data=[])


@router.get("/press/open/{machine_id}", response_model=Response, tags=["Press"])
async def open_press(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Opens the press.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the press status.
    """

    # MQTT
    try:
        print("MQTT message sent to open press.")
        # Publish a message to the press's MQTT topic to open the press.
        # This is a placeholder for the actual implementation.
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(success=False, msg=HTTPMessages.PRESS_OPEN_FAILED, data=[])

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.OpenPress
        )
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_PRESS_COMMAND, data=[]
        )

    # Create log entry
    await create_log_route(machine_id, PressLogType.OPEN_PRESS, None, db)

    return Response(success=True, msg=HTTPMessages.PRESS_OPENED, data=[])
