from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.database import Base

class TemperatureProfile(Base):
    """
    Represents the temperature_profiles table.

    Attributes:
        id (int): The primary key of the table.
        machine_id (int): Foreign key referencing the machines table.
        max_temp (float): The maximum temperature the oven can reach.
        safe_temp (float): The temperature considered safe for the oven.
        desired_temp (float): The target temperature during baking.
        bake_time_sec (int): The duration (in seconds) to bake.
    """

    __tablename__ = "temperature_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)

    max_temp = Column(Float, nullable=False)
    safe_temp = Column(Float, nullable=False)
    desired_temp = Column(Float, nullable=False)
    bake_time_sec = Column(Integer, nullable=False)

    label = Column(String(255), nullable=False, default="Unnamed Profile")

    # Relationship to the machine that owns this profile
    machine = relationship(
        "Machine",
        back_populates="temperature_profiles",
        foreign_keys=[machine_id],
    )

    # Relationship to the machine where this profile is active
    machines_using_profile = relationship(
        "Machine",
        primaryjoin="Machine.active_profile_id == TemperatureProfile.id",
        foreign_keys="[Machine.active_profile_id]",
        back_populates="active_profile",
    )
