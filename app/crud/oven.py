from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import (
    OvenBatch as OvenBatchORM,
    TemperatureLog as TemperatureLogORM,
    OvenLog as OvenLogORM,
    TemperatureProfile as TemperatureProfileORM,
    Machine as MachineORM,
)

from app.schemas import (
    OvenBatchCreate,
    TemperatureLogCreate,
    OvenLogCreate,
    TemperatureProfileCreate,
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

    query = (
        db.query(OvenBatchORM)
        .filter(OvenBatchORM.machine_id == machine_id)
        .order_by(desc(OvenBatchORM.start_time))
    )

    if limit is not None:
        query = query.limit(limit)

    return query.all()


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


def create_log(db: Session, log: OvenLogCreate) -> OvenLogORM:
    """
    Creates a log for the oven.

    Args:
        db (Session): The database session.
        log (OvenLogCreate): The log details.

    Returns:
        OvenLogCreate: The response containing the log details.
    """

    try:
        new_log = OvenLogORM(
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
) -> list[OvenLogORM] | None:
    """
    Retrieves the logs for a machine. Option to specify the limit.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.
        limit (int | None): The limit of the number of logs to retrieve.

    Returns:
        list[OvenLogORM] | None: The list of logs.
    """

    if limit is None:
        return db.query(OvenLogORM).filter(OvenLogORM.machine_id == machine_id).all()

    return (
        db.query(OvenLogORM)
        .filter(OvenLogORM.machine_id == machine_id)
        .limit(limit)
        .all()
    )


def create_temperature_profile(
    db: Session, temperature_profile: TemperatureProfileCreate
) -> TemperatureProfileORM:
    """
    Creates a temperature profile for the oven.

    Args:
        db (Session): The database session.
        temperature_profile (TemperatureProfileCreate): The temperature profile details.

    Returns:
        TemperatureProfileORM: The response containing the profile details.
    """

    try:
        new_profile = TemperatureProfileORM(
            label=temperature_profile.label,
            max_temp=temperature_profile.max_temp,
            safe_temp=temperature_profile.safe_temp,
            desired_temp=temperature_profile.desired_temp,
            bake_time_sec=temperature_profile.bake_time_sec,
            machine_id=temperature_profile.machine_id,
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return new_profile
    except Exception as e:
        db.rollback()
        raise e


def get_temperature_profiles_for_machine(
    db: Session, machine_id: int
) -> list[TemperatureProfileORM]:
    """
    Retrieves the temperature profiles for a machine.

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.

    Returns:
        list[TemperatureProfileORM]: The list of temperature profiles.
    """

    return (
        db.query(TemperatureProfileORM)
        .filter(TemperatureProfileORM.machine_id == machine_id)
        .all()
    )


def delete_temperature_profile(db: Session, profile_id: int) -> bool:
    """
    Deletes a temperature profile for the oven.

    Args:
        db (Session): The database session.
        profile_id (int): The profile identifier.

    Returns:
        bool: The response indicating the success of the operation.
    """

    try:
        db.query(TemperatureProfileORM).filter(
            TemperatureProfileORM.id == profile_id
        ).delete()
        db.commit()

        return True
    except Exception as e:
        db.rollback()
        raise e


def get_active_temperature_profile_for_machine(
    db: Session, machine_id: int
) -> TemperatureProfileORM | None:
    """
    Retrieves the active temperature profile for a machine by looking at the active id in the machines table

    Args:
        db (Session): The database session.
        machine_id (int): The machine identifier.

    Returns:
        TemperatureProfileORM | None: The response containing the profile details.
    """

    # Get the machine
    machine: MachineORM = (
        db.query(MachineORM).filter(MachineORM.id == machine_id).first()
    )

    # If no active profile, get the first profile and set it as active
    if machine.active_profile_id is None:
        active_profile = (
            db.query(TemperatureProfileORM)
            .filter(TemperatureProfileORM.machine_id == machine_id)
            .first()
        )

        if active_profile:
            machine.active_profile_id = active_profile.id
            db.commit()
            db.refresh(machine)
    else:
        active_profile = (
            db.query(TemperatureProfileORM)
            .filter(TemperatureProfileORM.id == machine.active_profile_id)
            .first()
        )

    return active_profile
