from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Machine(Base):
    """
    Represents the machines table.

    Attributes:
        id (int): The primary key of the table.
        name (str): The name of the machine.
        active_profile_id (int | None): The active profile id of the machine.
    """

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    # Foreign key to the active profile
    active_profile_id = Column(
        Integer, ForeignKey("temperature_profiles.id"), nullable=True
    )

    # Relationship to the active profile
    active_profile = relationship(
        "TemperatureProfile",
        primaryjoin="Machine.active_profile_id == TemperatureProfile.id",
        foreign_keys=[active_profile_id],
        back_populates="machines_using_profile",
        lazy="joined",  # Optional: Eager load to avoid extra queries
    )

    # Relationship to all temperature profiles for this machine
    temperature_profiles = relationship(
        "TemperatureProfile",
        back_populates="machine",
        foreign_keys="[TemperatureProfile.machine_id]",
        lazy="select",  # Optional: Load on-demand
    )

    oven_logs = relationship("OvenLog", back_populates="machine")
    press_logs = relationship("PressLog", back_populates="machine")

    oven_batches = relationship("OvenBatch", back_populates="machine")
    temperature_logs = relationship("TemperatureLog", back_populates="machine")
