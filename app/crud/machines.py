from sqlalchemy.orm import Session

from app.models import Machine as MachineORM

from app.schemas import (
    MachineCreate,
    MachineUpdate,
)


def create_machine(db: Session, machine: MachineCreate) -> MachineORM:
    """
    Creates a machine.

    Args:
        db (Session): The database session.
        machine (MachineCreate): The machine to be created.

    Returns:
        MachineORM: The created machine.
    """

    try:
        new_machine = MachineORM(**machine.dict())
        db.add(new_machine)
        db.commit()
        db.refresh(new_machine)
        return new_machine
    except Exception as e:
        db.rollback()
        raise e


def get_machine(db: Session, machine_id: int) -> MachineORM:
    """
    Retrieves a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine ID.

    Returns:
        MachineORM: The retrieved machine.
    """

    return db.query(MachineORM).filter(MachineORM.id == machine_id).first()


def get_machines(db: Session, limit: int | None = 100) -> list[MachineORM]:
    """
    Retrieves all the machines.

    Args:
        db (Session): The database session.

    Returns:
        list[MachineORM]: The list of machines.
    """

    if limit is None:
        return db.query(MachineORM).all()

    return db.query(MachineORM).limit(limit).all()


def update_machine(db: Session, machine_id: int, machine: MachineUpdate) -> MachineORM:
    """
    Updates a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine ID.
        machine (MachineUpdate): The machine to be updated.

    Returns:
        MachineORM: The updated machine.
    """

    try:
        db_machine = db.query(MachineORM).filter(MachineORM.id == machine_id).first()

        for key, value in machine.dict(exclude_unset=True).items():
            setattr(db_machine, key, value)

        db.commit()
        db.refresh(db_machine)

        return db_machine
    except Exception as e:
        db.rollback()
        raise e


def delete_machine(db: Session, machine_id: int) -> MachineORM:
    """
    Deletes a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine ID.

    Returns:
        MachineORM: The deleted machine.
    """

    try:
        db_machine = db.query(MachineORM).filter(MachineORM.id == machine_id).first()
        db.delete(db_machine)
        db.commit()
        return db_machine
    except Exception as e:
        db.rollback()
        raise e


def set_machine_active_temperature_profile(
    db: Session, machine_id: int, profile_id: int
) -> MachineORM:
    """
    Sets the active temperature profile for a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine ID.
        profile_id (int): The profile ID.

    Returns:
        MachineORM: The updated machine.
    """

    try:
        db_machine = db.query(MachineORM).filter(MachineORM.id == machine_id).first()
        db_machine.active_profile_id = profile_id
        db.commit()
        db.refresh(db_machine)
        return db_machine
    except Exception as e:
        db.rollback()
        raise e
