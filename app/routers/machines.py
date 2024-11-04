from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages

from app.schemas import (
    Response,
    MachineCreate,
    MachineUpdate,
    Machine,
)

from app.crud.machines import (
    create_machine,
    get_machine,
    get_machines,
    update_machine,
    delete_machine,
)

from app.websocket import manager as WebSocketManager


router = APIRouter()


@router.post("/machines", response_model=Response, tags=["Machines"])
def create_machine_route(
    machine: MachineCreate,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a machine.

    Args:
        machine (MachineCreate): The machine to be created.
        db (Session): The database session.

    Returns:
        Response: The response containing the created machine.
    """

    new_machine: MachineCreate = create_machine(db, machine)

    return Response(
        success=True,
        msg=HTTPMessages.MACHINE_CREATED,
        data=[new_machine],
    )


@router.get("/machine/{machine_id}", response_model=Response, tags=["Machines"])
def get_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves a machine.

    Args:
        machine_id (int): The machine ID.
        db (Session): The database session.

    Returns:
        Response: The response containing the retrieved machine.
    """

    machine: Machine = get_machine(db, machine_id)

    return Response(
        success=True,
        msg=HTTPMessages.MACHINE_RETRIEVED,
        data=[machine],
    )


@router.get("/machines", response_model=Response, tags=["Machines"])
def get_machines_route(
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves all the machines.

    Args:
        db (Session): The database session.

    Returns:
        Response: The response containing the list of machines.
    """

    machines: list[Machine] = get_machines(db, limit=None)

    return Response(
        success=True,
        msg=HTTPMessages.MACHINES_RETRIEVED,
        data=machines,
    )


@router.put("/machine/{machine_id}", response_model=Response, tags=["Machines"])
def update_machine_route(
    machine_id: int,
    machine: MachineUpdate,
    db: Session = Depends(get_db),
) -> Response:
    """
    Updates a machine.

    Args:
        machine_id (int): The machine ID.
        machine (MachineUpdate): The machine details to be updated.
        db (Session): The database session.

    Returns:
        Response: The response containing the updated machine.
    """

    updated_machine: Machine = update_machine(db, machine_id, machine)

    return Response(
        success=True,
        msg=HTTPMessages.MACHINE_UPDATED,
        data=[updated_machine],
    )


@router.delete("/machine/{machine_id}", response_model=Response, tags=["Machines"])
def delete_machine_route(
    machine_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """
    Deletes a machine.

    Args:
        machine_id (int): The machine ID.
        db (Session): The database session.

    Returns:
        Response: The response containing the deleted machine.
    """

    deleted_machine: Machine = delete_machine(db, machine_id)

    return Response(
        success=True,
        msg=HTTPMessages.MACHINE_DELETED,
        data=[deleted_machine],
    )


@router.get("/machine/{machine_id}/hmi-connected", response_model=Response, tags=["Machines"])
def check_hmi_connected(
    machine_id: int,
) -> Response:
    """
    Checks if the HMI is connected to the machine.

    Args:
        machine_id (int): The machine ID.

    Returns:
        Response: The response containing the HMI connection status.
    """

    hmi_connected: bool = WebSocketManager.is_client_connected(machine_id)

    return Response(
        success=True,
        msg=HTTPMessages.CONNECTION_STATUS_RETRIEVED,
        data=hmi_connected,
    )