from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from app.database import Base
from sqlalchemy.orm import relationship

from datetime import datetime, timezone
from app.utils.logs_enums import LogType, PressLogDescription


class PressLog(Base):
    """
    Represents the press_logs table.

    Attributes:
        id (int): The primary key of the table.
        batch_id (int): The batch id.
        type (oven_log_types): The type of log.
        description (oven_log_description): The description of the log.
        created_at (datetime): The timestamp when the log was created.

    Table Name:
        press_logs
    """

    __tablename__ = "press_logs"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("oven_batches.id"))
    type = Column(Enum(LogType, name="log_type"), nullable=False)
    description = Column(
        Enum(PressLogDescription, name="press_log_description"), nullable=False
    )
    created_at = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    press_batch = relationship("PressBatch", back_populates="press_logs")
