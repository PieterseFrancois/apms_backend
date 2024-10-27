from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.utils.logs_enums import OvenLogType


class OvenLog(Base):
    """
    Represents the oven_logs table.

    Attributes:
        id (int): The primary key of the table.
        batch_id (int): The batch id.
        machine_id (int): The ID of the machine.
        type (OvenLogType): The type of log.
        created_at (datetime): The timestamp when the log was created.

    Table Name:
        oven_logs
    """

    __tablename__ = "oven_logs"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("oven_batches.id"), nullable=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    type = Column(Enum(OvenLogType, name="oven_log_type_enum"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))

    oven_batch = relationship("OvenBatch", back_populates="oven_logs")
    machine = relationship("Machine", back_populates="oven_logs")
