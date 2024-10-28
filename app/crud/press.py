from sqlalchemy.orm import Session

from app.models import (
    PressLog as PressLogORM,
)

from app.schemas import (
    PressLogCreate,
)

from datetime import datetime, timezone

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