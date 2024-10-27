from pydantic import BaseModel


class MachineBase(BaseModel):
    """
    Represents the base schema for the machines.

    Attributes:
        name (str): The name of the machine.
        active_profile_id (int | None): The active profile id of the machine.
    """

    name: str
    active_profile_id: int | None


class MachineCreate(MachineBase):
    """
    Represents the schema for creating a machine.

    Inherits:
        name (str): The name of the machine.
        active_profile_id (int | None): The active profile id of the machine.
    """

    pass


class MachineUpdate(MachineBase):
    """
    Represents the schema for updating a machine.

    Inherits:
        name (str): The name of the machine.
        active_profile_id (int | None): The active profile id of the machine.
    """

    pass


class Machine(MachineBase):
    """
    Represents the schema for the machines.

    Attributes:
        id (int): The primary key of the table.

    Inherits:
        name (str): The name of the machine.
        active_profile_id (int | None): The active profile id of the machine.
    """

    id: int

    class Config:
        from_attributes = True
