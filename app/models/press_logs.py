from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from app.database import Base
from sqlalchemy.orm import relationship

from datetime import datetime, timezone
from app.utils.logs_enums import PressLogType


class PressLog(Base):
    """
    Represents the press_logs table with the updated ENUM type.

    Attributes:
        id (int): The primary key of the table.
        batch_id (int): The batch id.
        machine_id (int): The ID of the machine.
        type (PressLogType): The type of log (new ENUM type).
        created_at (datetime): The timestamp when the log was created.

    Table Name:
        press_logs
    """

    __tablename__ = "press_logs"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("press_batches.id"), nullable=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    type = Column(Enum(PressLogType, name="press_log_type_enum"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))

    press_batch = relationship("PressBatch", back_populates="press_logs")
    machine = relationship("Machine", back_populates="press_logs")
