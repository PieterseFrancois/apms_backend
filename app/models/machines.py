from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


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

    temperature_logs = relationship("TemperatureLog", back_populates="machine")
