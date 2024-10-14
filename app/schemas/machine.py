from pydantic import BaseModel


class MachineBase(BaseModel):
    """
    Represents the base schema for the machines.

    Attributes:
        name (str): The name of the machine.
    """

    name: str


class MachineCreate(MachineBase):
    """
    Represents the schema for creating a machine.

    Inherits:
        MachineBase
    """

    pass


class MachineUpdate(MachineBase):
    """
    Represents the schema for updating a machine.

    Inherits:
        MachineBase
    """

    pass


class Machine(MachineBase):
    """
    Represents the schema for the machines.

    Inherits:
        MachineBase
    """

    id: int

    class Config:
        from_attributes = True
