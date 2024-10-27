from pydantic import BaseModel


class TemperatureProfileBase(BaseModel):
    """
    Represents the temperature profile schema.

    Attributes:
        label (str): The name of the profile.
        max_temp (float): The maximum temperature the oven can reach.
        safe_temp (float): The temperature considered safe for the oven.
        desired_temp (float): The target temperature during baking.
        bake_time_sec (int): The duration (in seconds) to bake.

    """

    label: str
    max_temp: float
    safe_temp: float
    desired_temp: float
    bake_time_sec: int

    class Config:
        from_attributes = True


class TemperatureProfileCreate(TemperatureProfileBase):
    """
    Represents the temperature profile schema for creation.

    Attributes:
        machine_id (int): The machine ID.

    Inherits:
        label (str): The name of the profile.
        max_temp (float): The maximum temperature the oven can reach.
        safe_temp (float): The temperature considered safe for the oven.
        desired_temp (float): The target temperature during baking.
        bake_time_sec (int): The duration (in seconds) to bake.
    """

    machine_id: int


class TemperatureProfile(TemperatureProfileBase):
    """
    Represents the temperature profile schema for response.

    Attributes:
        id (int): The primary key of the table.
        machine_id (int): The machine ID.

    Inherits:
        label (str): The name of the profile.
        max_temp (float): The maximum temperature the oven can reach.
        safe_temp (float): The temperature considered safe for the oven.
        desired_temp (float): The target temperature during baking.
        bake_time_sec (int): The duration (in seconds) to bake.
    """

    id: int
    machine_id: int

    class Config:
        from_attributes = True
