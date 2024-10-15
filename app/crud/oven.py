from sqlalchemy.orm import Session

from app.models import (
    OvenBatch as OvenBatchORM,
    TemperatureLog as TemperatureLogORM,
)

from app.schemas import (
    OvenBatchCreate,
    TemperatureLogCreate,
)

from app.utils.state_enum import BatchState

from datetime import datetime, timezone


def create_oven_batch(db: Session, oven_batch: OvenBatchCreate) -> OvenBatchORM:
    """
    Creates an oven batch.

    Args:
        db (Session): The database session.
        oven_batch (OvenBatchCreate): The oven batch details.

    Returns:
        OvenBatchORM: The response containing the batch details.
    """

    try:
        new_oven_batch = OvenBatchORM(
            start_time=oven_batch.start_time,
            state=oven_batch.state.value,
            machine_id=oven_batch.machine_id,
        )
        db.add(new_oven_batch)
        db.commit()
        db.refresh(new_oven_batch)

        return new_oven_batch
    except Exception as e:
        db.rollback()
        raise e


def get_oven_batch(db: Session, batch_id: int) -> OvenBatchORM:
    """
    Retrieves an oven batch by the identifier.

    Args:
        db (Session): The database session.
        batch_id (int): The batch identifier.

    Returns:
        OvenBatchORM: The response containing the batch details.
    """

    return db.query(OvenBatchORM).filter(OvenBatchORM.id == batch_id).first()


def get_oven_batches_for_machine(
    db: Session, machine_id: int, limit: int | None = 100
) -> list[OvenBatchORM] | None:
    """
    Retrieves all the oven batches.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.
        limit (int | None): The limit of the number of batches to retrieve.

    Returns:
        list[OvenBatchORM] | None: The list of oven batches.
    """

    if limit is None:
        return (
            db.query(OvenBatchORM).filter(OvenBatchORM.machine_id == machine_id).all()
        )

    return (
        db.query(OvenBatchORM)
        .filter(OvenBatchORM.machine_id == machine_id)
        .limit(limit)
        .all()
    )


def get_active_oven_batches(db: Session) -> OvenBatchORM:
    """
    Retrieves the active oven batch.

    Args:
        db (Session): The database session.

    Returns:
        OvenBatchORM: The response containing the active batch details.
    """

    return db.query(OvenBatchORM).filter(OvenBatchORM.state == BatchState.ACTIVE).all()


def get_latest_oven_batch_for_machine(
    db: Session, machine_id: int
) -> OvenBatchORM | None:
    """
    Retrieves the latest oven batch for a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.

    Returns:
        OvenBatchORM | None: The response containing the latest batch details.
    """

    return (
        db.query(OvenBatchORM)
        .filter(OvenBatchORM.machine_id == machine_id)
        .order_by(OvenBatchORM.start_time.desc())
        .first()
    )


def stop_active_oven_batch(db: Session, machine_id: int) -> OvenBatchORM:
    """
    Stops the active oven batch.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.

    Returns:
        OvenBatchORM: The response containing the updated batch details.
    """

    try:
        # Get all actives batches
        active_batch = (
            db.query(OvenBatchORM)
            .filter(OvenBatchORM.state == BatchState.ACTIVE)
            .filter(OvenBatchORM.machine_id == machine_id)
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


def delete_oven_batch(db: Session, batch_id: int) -> bool:
    """
    Deletes an oven batch by the identifier.

    Args:
        db (Session): The database session.
        batch_id (int): The batch identifier.

    Returns:
        bool: The response indicating the success of the operation.
    """

    try:
        db.query(OvenBatchORM).filter(OvenBatchORM.id == batch_id).delete()
        db.commit()

        return True
    except Exception as e:
        db.rollback()
        raise e


def create_temperature_log(
    db: Session, temperature_log: TemperatureLogCreate
) -> TemperatureLogORM:
    """
    Creates a temperature log for the oven.

    Args:
        db (Session): The database session.
        temperature (TemperatureLogCreate): The temperature log details.

    Returns:
        TemperatureLogORM: The response containing the log details.
    """

    try:
        temperature_log = TemperatureLogORM(
            temperature=temperature_log.temperature,
            machine_id=temperature_log.machine_id,
            batch_id=temperature_log.batch_id,
            created_at=datetime.now(tz=timezone.utc),
        )

        db.add(temperature_log)
        db.commit()
        db.refresh(temperature_log)

        return temperature_log
    except Exception as e:
        db.rollback()
        raise e


def get_temperature_logs_for_batch(
    db: Session, batch_id: int
) -> list[TemperatureLogORM]:
    """
    Retrieves the temperature logs for a batch.

    Args:
        db (Session): The database session.
        batch_id (int): The batch identifier.

    Returns:
        list[TemperatureLogORM]: The list of temperature logs.
    """

    return (
        db.query(TemperatureLogORM).filter(TemperatureLogORM.batch_id == batch_id).all()
    )


def get_temperature_logs_for_machine(
    db: Session, machine_id: int, limit: int | None = None
) -> list[TemperatureLogORM]:
    """
    Retrieves the temperature logs for a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.
        limit (int | None): The limit of the number of logs to retrieve.

    Returns:
        list[TemperatureLogORM]: The list of temperature logs.
    """

    if limit is None:
        return (
            db.query(TemperatureLogORM)
            .filter(TemperatureLogORM.machine_id == machine_id)
            .all()
        )

    return (
        db.query(TemperatureLogORM)
        .filter(TemperatureLogORM.machine_id == machine_id)
        .limit(limit)
        .all()
    )
