from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Machine(Base):
    """
    Represents the machines table.

    Attributes:
        id (int): The primary key of the table.
        name (str): The name of the machine.

    Table Name:
        machines
    """

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    oven_logs = relationship("OvenLog", back_populates="machine")
    press_logs = relationship("PressLog", back_populates="machine")

    oven_batches = relationship("OvenBatch", back_populates="machine")
    temperature_logs = relationship("TemperatureLog", back_populates="machine")
