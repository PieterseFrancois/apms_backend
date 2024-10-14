from sqlalchemy.orm import Session

from app.models import TemperatureLog as TemperatureLogORM

from app.schemas import (
    TemperatureLogBase,
)

from datetime import datetime, timezone


def create_temperature_log(db: Session, temperature: float) -> TemperatureLogORM:
    """
    Creates a temperature log for the oven.

    Args:
        db (Session): The database session.
        temperature (float): The temperature value.

    Returns:
        TemperatureLogORM: The response containing the log details.
    """

    try:
        temperature_log = TemperatureLogORM(
            temperature=temperature, created_at=datetime.now(tz=timezone.utc)
        )

        db.add(temperature_log)
        db.commit()
        db.refresh(temperature_log)

        return temperature_log
    except Exception as e:
        db.rollback()
        raise e


def get_temperature_logs(
    db: Session, limit: int | None = 100
) -> list[TemperatureLogBase]:
    """
    Retrieves all the temperature logs.

    Args:
        db (Session): The database session.

    Returns:
        list[TemperatureLogBase]: The list of temperature logs.
    """

    if limit is None:
        return db.query(TemperatureLogORM).all()

    return db.query(TemperatureLogORM).limit(limit).all()
