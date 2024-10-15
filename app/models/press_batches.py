from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.state_enum import BatchState


class PressBatch(Base):
    """
    Represents the press_batches table.

    Attributes:
        id (int): The primary key of the table.
        start_time (datetime): The start time of the batch.
        stop_time (datetime): The stop time of the batch.
        state (BatchState): The state of the batch.
        machine_id (int): The machine id.

    Table Name:
        press_batches
    """

    __tablename__ = "press_batches"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    stop_time = Column(DateTime)
    state = Column(Enum(BatchState, name="batch_state_enum"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"))
    press_logs = relationship("PressLog", back_populates="press_batch")
