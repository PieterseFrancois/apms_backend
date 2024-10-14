from app.database import Base

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class TemperatureLog(Base):
    """
    Represents the temperature logs table.

    Attributes:
        id (int): The primary key of the table.
        temperature (float): The temperature value.
        created_at (datetime): The timestamp when the log was created

    Table Name:
        temperature_logs
    """

    __tablename__ = "temperature_logs"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    machine_id = Column(Integer, ForeignKey("machines.id"))
    batch_id = Column(Integer, ForeignKey("oven_batches.id"))

    machine = relationship("Machine", back_populates="temperature_logs")
    oven_batch = relationship("OvenBatch", back_populates="temperature_logs")
