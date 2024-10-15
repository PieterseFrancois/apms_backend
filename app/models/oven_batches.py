from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.state_enum import BatchState


class OvenBatch(Base):
    """
    Represents the oven_batches table.

    Attributes:
        id (int): The primary key of the table.
        start_time (datetime): The start time of the batch.
        stop_time (datetime): The stop time of the batch.
        state (BatchState): The state of the batch.
        machine_id (int): The machine identifier.

    Table Name:
        oven_batches
    """

    __tablename__ = "oven_batches"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    stop_time = Column(DateTime)
    state = Column(Enum(BatchState, name="batch_state_enum"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"))

    oven_logs = relationship("OvenLog", back_populates="oven_batch")
    temperature_logs = relationship("TemperatureLog", back_populates="oven_batch")
    machine = relationship("Machine", back_populates="oven_batches")
