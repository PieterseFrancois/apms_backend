from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.websocket import manager as WebSocketManager
from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages
from app.utils.message_identifiers import MessageIdentifiers
from app.utils.logs_enums import PressLogType

from app.schemas import (
    Response,
    PressLogCreate,
    PressLog,
    PressLogExpanded,
)

from app.crud.press import (
    create_log,
    get_logs_for_machine,
)

from datetime import datetime, timezone

router = APIRouter()


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

    await WebSocketManager.send_personal_message(
        created_log_dict, machine_id, MessageIdentifiers.PressLog
    )

    return Response(success=True, msg=HTTPMessages.PRESS_LOG_CREATED, data=[created_log])


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