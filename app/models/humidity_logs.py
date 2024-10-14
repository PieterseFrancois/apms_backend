from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.database import Base

from datetime import datetime, timezone


class HumidityLog(Base):
    """
    Represents the humidity_logs table.

    Attributes:
        id (int): The primary key of the table.
        humidity (float): The humidity value.
        created_at (datetime): The timestamp when the log was created.
        machine_id (int): The machine id.
        batch_id (int): The batch id.

    Table Name:
        humidity_logs
    """

    __tablename__ = "humidity_logs"

    id = Column(Integer, primary_key=True)
    humidity = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    machine_id = Column(Integer, ForeignKey("machines.id"))
    batch_id = Column(Integer, ForeignKey("oven_batches.id"))
