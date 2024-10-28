from sqlalchemy.orm import Session

from app.models import (
    PressBatch as PressBatchORM,
    PressLog as PressLogORM,
)

from app.schemas import (
    PressBatchCreate,
    PressLogCreate,
)

from app.utils.state_enum import BatchState

from datetime import datetime, timezone


def create_press_batch(db: Session, press_batch: PressBatchCreate) -> PressBatchORM:
    """
    Creates a press batch.

    Args:
        db (Session): The database session.
        press_batch (PressBatchCreate): The press batch details.

    Returns:
        PressBatchORM: The response containing the batch details.
    """

    try:
        new_press_batch = PressBatchORM(
            start_time=press_batch.start_time,
            state=press_batch.state.value,
            machine_id=press_batch.machine_id,
        )
        db.add(new_press_batch)
        db.commit()
        db.refresh(new_press_batch)

        return new_press_batch
    except Exception as e:
        db.rollback()
        raise e


def get_press_batch(db: Session, batch_id: int) -> PressBatchORM:
    """
    Retrieves a press batch by the identifier.

    Args:
        db (Session): The database session.
        batch_id (int): The batch identifier.

    Returns:
        PressBatchORM: The response containing the batch details.
    """

    return db.query(PressBatchORM).filter(PressBatchORM.id == batch_id).first()


def get_press_batches_for_machine(
    db: Session, machine_id: int, limit: int | None = 100
) -> list[PressBatchORM] | None:
    """
    Retrieves all the press batches.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.
        limit (int | None): The limit of the number of batches to retrieve.

    Returns:
        list[PressBatchORM] | None: The list of press batches.
    """

    if limit is None:
        return (
            db.query(PressBatchORM).filter(PressBatchORM.machine_id == machine_id).all()
        )

    return (
        db.query(PressBatchORM)
        .filter(PressBatchORM.machine_id == machine_id)
        .limit(limit)
        .all()
    )


def get_active_press_batches(db: Session) -> PressBatchORM:
    """
    Retrieves the active press batch.

    Args:
        db (Session): The database session.

    Returns:
        PressBatchORM: The response containing the active batch details.
    """

    return (
        db.query(PressBatchORM).filter(PressBatchORM.state == BatchState.ACTIVE).all()
    )


def get_latest_press_batch_for_machine(
    db: Session, machine_id: int
) -> PressBatchORM | None:
    """
    Retrieves the latest press batch for a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.

    Returns:
        PressBatchORM | None: The response containing the latest batch details.
    """

    return (
        db.query(PressBatchORM)
        .filter(PressBatchORM.machine_id == machine_id)
        .order_by(PressBatchORM.start_time.desc())
        .first()
    )


def stop_active_press_batch(db: Session, machine_id: int) -> PressBatchORM:
    """
    Stops the active press batch.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.

    Returns:
        PressBatchORM: The response containing the updated batch details.
    """

    try:
        # Get all actives batches
        active_batch = (
            db.query(PressBatchORM)
            .filter(PressBatchORM.state == BatchState.ACTIVE)
            .filter(PressBatchORM.machine_id == machine_id)
            .first()
        )

        if active_batch:
            active_batch.state = BatchState.COMPLETED.value
            active_batch.stop_time = datetime.now(tz=timezone.utc)

            db.commit()

        return active_batch
    except Exception as e:
        db.rollback()
        raise e


def delete_press_batch(db: Session, batch_id: int) -> bool:
    """
    Deletes a press batch by the identifier.

    Args:
        db (Session): The database session.
        batch_id (int): The batch identifier.

    Returns:
        bool: The response indicating the success of the operation.
    """

    try:
        db.query(PressBatchORM).filter(PressBatchORM.id == batch_id).delete()
        db.commit()

        return True
    except Exception as e:
        db.rollback()
        raise e


def create_log(db: Session, log: PressLogCreate) -> PressLogORM:
    """
    Creates a log for the press.

    Args:
        db (Session): The database session.
        log (PressLogCreate): The log details.

    Returns:
        PressLogCreate: The response containing the log details.
    """

    try:
        new_log = PressLogORM(
            machine_id=log.machine_id,
            type=log.type,
            batch_id=log.batch_id,
            created_at=datetime.now(tz=timezone.utc),
        )

        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        return new_log
    except Exception as e:
        db.rollback()
        raise e


def get_logs_for_machine(
    db: Session, machine_id: int, limit: int | None = 100
) -> list[PressLogORM] | None:
    """
    Retrieves the logs for a machine. Option to specify the limit.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.
        limit (int | None): The limit of the number of logs to retrieve.

    Returns:
        list[PressLogORM] | None: The list of logs.
    """

    if limit is None:
        return db.query(PressLogORM).filter(PressLogORM.machine_id == machine_id).all()

    return (
        db.query(PressLogORM)
        .filter(PressLogORM.machine_id == machine_id)
        .limit(limit)
        .all()
    )
