from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.websocket import manager as WebSocketManager
from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages
from app.utils.message_identifiers import MessageIdentifiers
from app.utils.state_enum import BatchState
from app.utils.logs_enums import OvenLogType

from app.schemas import (
    Response,
    OvenBatchCreate,
    OvenBatch,
    TemperatureLogBase,
    TemperatureLogCreate,
    TemperatureLog,
    OvenLogCreate,
    OvenLog,
    OvenLogExpanded,
    TemperatureProfileBase,
    TemperatureProfileCreate,
    TemperatureProfile,
    Machine,
)

from app.crud.oven import (
    create_oven_batch,
    get_latest_oven_batch_for_machine,
    get_oven_batches_for_machine,
    stop_active_oven_batch,
    create_temperature_log,
    get_temperature_logs_for_batch,
    get_temperature_logs_for_machine,
    create_log,
    get_logs_for_machine,
    create_temperature_profile,
    get_temperature_profiles_for_machine,
    delete_temperature_profile,
    get_active_temperature_profile_for_machine,
)

from app.crud.machines import (
    set_machine_active_temperature_profile,
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
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        stop_active_oven_batch(db, machine_id)

        return Response(success=False, msg=HTTPMessages.OVEN_START_FAILED, data=[])

    # Websocket
    try:
        await WebSocketManager.send_personal_message(
            "", machine_id, MessageIdentifiers.BakeBatch
        )
    except Exception:
        # Create log entry
        # create_log_route(machine_id, OvenLogType.ERROR, None, db)

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_OVEN_COMMAND, data=[]
        )

    # Create log entry
    await create_log_route(machine_id, OvenLogType.BAKE_BATCH, None, db)

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
    except Exception:
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
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.

        return Response(
            success=False, msg=HTTPMessages.WEBSOCKET_FAILURE_OVEN_COMMAND, data=[]
        )

    # Create log entry
    await create_log_route(machine_id, OvenLogType.STOP_BAKE, None, db)

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

    oven_batch: OvenBatch | None = get_latest_oven_batch_for_machine(db, machine_id)

    return Response(
        success=True, msg=HTTPMessages.OVEN_STATUS_RETRIEVED, data=[oven_batch]
    )


@router.get("/oven/batches/{machine_id}", response_model=Response, tags=["Oven"])
def get_oven_batches_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the oven batches for a machine.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the oven batches.
    """

    oven_batches: list[OvenBatch] | None = get_oven_batches_for_machine(db, machine_id)

    return Response(
        success=True, msg=HTTPMessages.OVEN_STATUS_RETRIEVED, data=oven_batches
    )


@router.post(
    "/oven/log/temperature/{machine_id}",
    response_model=Response,
    tags=["Oven - Temperature"],
)
async def create_temperature_log_route(
    machine_id: int,
    temperature: float,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a temperature log for the oven.

    Args:
        machine_id (int): The machine identifier.
        temperature (float): The temperature value.
        db (Session): The database session.

    Returns:
        Response: The response containing the log details.
    """

    # Get the machines latest batch
    latest_batch: OvenBatch = get_latest_oven_batch_for_machine(db, machine_id)

    # Check if a batch is active
    if latest_batch is None:
        batch_id = None
    elif latest_batch.state != BatchState.ACTIVE:
        batch_id = None
    else:
        batch_id = latest_batch.id

    # Create new temperature log entry
    new_temperature_log = TemperatureLogCreate(
        temperature=temperature,
        machine_id=machine_id,
        batch_id=batch_id,
    )

    temperature_log: TemperatureLogBase = create_temperature_log(
        db, new_temperature_log
    )

    temperature_log = TemperatureLogBase(
        temperature=temperature_log.temperature,
        created_at=temperature_log.created_at,
        machine_id=temperature_log.machine_id,
        batch_id=temperature_log.batch_id,
    )

    # Broadcast the temperature log to all connected clients of the machine id
    await WebSocketManager.send_personal_message(
        temperature_log.dict(), machine_id, MessageIdentifiers.CurrentTemp
    )

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_LOG_CREATED,
        data=[temperature_log],
    )


@router.get(
    "/oven/logs/temperature/{machine_id}",
    response_model=Response,
    tags=["Oven - Temperature"],
)
def get_temperature_logs_for_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the temperature logs for the oven based on the machine identifier.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the temperature logs.
    """

    temperature_logs: list[TemperatureLog] = get_temperature_logs_for_machine(
        db, machine_id
    )

    return Response(
        success=True, msg=HTTPMessages.TEMPERATURE_LOGS_RETRIEVED, data=temperature_logs
    )


@router.get(
    "/oven/logs/temperature/batch/{batch_id}",
    response_model=Response,
    tags=["Oven - Temperature"],
)
def get_temperature_logs_for_batch_route(
    batch_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the temperature logs for the oven based on the batch identifier.

    Args:
        batch_id (int): The batch identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the temperature logs.
    """

    temperature_logs: list[TemperatureLog] = get_temperature_logs_for_batch(
        db, batch_id
    )

    return Response(
        success=True, msg=HTTPMessages.TEMPERATURE_LOGS_RETRIEVED, data=temperature_logs
    )


@router.post("/oven/log/{machine_id}", response_model=Response, tags=["Oven - Log"])
async def create_log_route(
    machine_id: int,
    type: OvenLogType,
    batch_id: int | None = None,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a log for the oven.

    Args:
        machine_id (int): The machine identifier.
        type (OvenLogType): The type of log.
        batch_id (int | None): The batch identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the log details.
    """

    new_log = OvenLogCreate(
        machine_id=machine_id,
        type=type,
        batch_id=batch_id,
    )

    log: OvenLog = create_log(db, new_log)

    created_log = OvenLogExpanded(
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

    await WebSocketManager.send_personal_message(
        created_log_dict, machine_id, MessageIdentifiers.OvenLog
    )

    return Response(success=True, msg=HTTPMessages.OVEN_LOG_CREATED, data=[created_log])


@router.get("/oven/logs/{machine_id}", response_model=Response, tags=["Oven - Log"])
def get_logs_for_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the logs for the oven based on the machine identifier.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the logs.
    """

    logs: list[OvenLog] = get_logs_for_machine(db, machine_id)

    expanded_logs = [
        OvenLogExpanded(
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
        success=True, msg=HTTPMessages.OVEN_LOGS_RETRIEVED, data=expanded_logs
    )


@router.post(
    "/oven/profile/{machine_id}", response_model=Response, tags=["Oven - Profile"]
)
def create_temperature_profile_route(
    machine_id: int,
    temperature_profile: TemperatureProfileBase,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a temperature profile for the oven.

    Args:
        machine_id (int): The machine identifier.
        temperature_profile (TemperatureProfileBase): The temperature profile.
        db (Session): The database session.

    Returns:
        Response: The response containing the temperature profile.
    """

    new_temperature_profile = TemperatureProfileCreate(
        label=temperature_profile.label,
        max_temp=temperature_profile.max_temp,
        safe_temp=temperature_profile.safe_temp,
        desired_temp=temperature_profile.desired_temp,
        bake_time_sec=temperature_profile.bake_time_sec,
        machine_id=machine_id,
    )

    temperature_profile: TemperatureProfileCreate = create_temperature_profile(
        db, new_temperature_profile
    )

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_PROFILE_CREATED,
        data=[temperature_profile],
    )


@router.get(
    "/oven/profiles/{machine_id}", response_model=Response, tags=["Oven - Profile"]
)
def get_temperature_profiles_for_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the temperature profiles for the oven based on the machine identifier.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the temperature profiles.
    """

    temperature_profiles: list[TemperatureProfile] = (
        get_temperature_profiles_for_machine(db, machine_id)
    )

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_PROFILES_RETRIEVED,
        data=temperature_profiles,
    )


@router.delete(
    "/oven/profile/{profile_id}", response_model=Response, tags=["Oven - Profile"]
)
def delete_temperature_profile_route(
    profile_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Deletes a temperature profile for the oven.

    Args:
        profile_id (int): The profile identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the temperature profile.
    """

    delete_temperature_profile(db, profile_id)

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_PROFILE_DELETED,
        data=[],
    )


@router.get(
    "/oven/{machine_id}/profile/set-active/{profile_id}",
    response_model=Response,
    tags=["Oven - Profile Active"],
)
async def set_machine_active_temperature_profile_route(
    machine_id: int,
    profile_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Sets the active temperature profile for a machine.

    Args:
        machine_id (int): The machine ID.
        profile_id (int): The profile ID.
        db (Session): The database session.

    Returns:
        Response: The response containing the updated machine.
    """

    updated_machine_orm = set_machine_active_temperature_profile(
        db, machine_id, profile_id
    )

    updated_machine: Machine = Machine(
        id=updated_machine_orm.id,
        name=updated_machine_orm.name,
        active_profile_id=updated_machine_orm.active_profile_id,
    )

    # Send the active profile to the machine
    try:
        await WebSocketManager.send_personal_message(
            updated_machine.dict(), machine_id, MessageIdentifiers.ActiveProfile
        )
    except Exception:
        # Create log entry
        # Placeholder for the actual implementation.
        pass

    return Response(
        success=True,
        msg=HTTPMessages.MACHINE_ACTIVE_PROFILE_SET,
        data=[updated_machine],
    )


@router.get(
    "/oven/{machine_id}/profile/get-active",
    response_model=Response,
    tags=["Oven - Profile Active"],
)
def get_active_temperature_profile_for_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves the active temperature profile for the oven based on the machine identifier.

    Args:
        machine_id (int): The machine identifier.
        db (Session): The database session.

    Returns:
        Response: The response containing the temperature profile.
    """

    temperature_profile: TemperatureProfile | None = (
        get_active_temperature_profile_for_machine(db, machine_id)
    )

    if temperature_profile is None:
        return Response(
            success=False,
            msg=HTTPMessages.NO_TEMPERATURE_PROFILES_FOUND,
            data=[],
        )

    return Response(
        success=True,
        msg=HTTPMessages.ACTIVE_TEMPERATURE_PROFILE_RETRIEVED,
        data=[temperature_profile],
    )
