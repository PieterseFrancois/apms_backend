from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.utils.http_messages import HTTPMessages

from app.schemas import (
    Response,
    TemperatureLogBase,
)

from app.crud.oven import (
    create_temperature_log,
    get_temperature_logs,
)

router = APIRouter()


@router.post("/oven/log/temperature", response_model=Response, tags=["Oven"])
def create_temperature_log_route(
    temperature: float,
    db: Session = Depends(get_db),
) -> Response:
    """
    Creates a temperature log for the oven.

    Parameters:
    - temperature (float): The temperature value.
    - db (Session): The database session.

    Returns:
    - Response: The response containing the log details.
    """

    result = create_temperature_log(db, temperature)

    temperature_log = TemperatureLogBase(
        temperature=result.temperature,
        created_at=result.created_at,
    )

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_LOG_CREATED,
        data=[temperature_log],
    )


@router.get("/oven/logs/temperature", response_model=Response, tags=["Oven"])
def get_temperature_logs_route(
    db: Session = Depends(get_db),
) -> Response:
    """
    Retrieves all the temperature logs.

    Parameters:
    - db (Session): The database session.

    Returns:
    - Response: The response containing the list of temperature logs.
    """

    temperature_logs: list[TemperatureLogBase] = get_temperature_logs(db)

    return Response(
        success=True,
        msg=HTTPMessages.TEMPERATURE_LOGS_RETRIEVED,
        data=temperature_logs,
    )
