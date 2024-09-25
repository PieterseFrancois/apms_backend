from enum import Enum

class HTTPMessages(Enum):
    """
    Represents the HTTP messages associated with an API response.
    """

    VALIDATION_ERROR = "Validation error."
    DATA_INTEGRITY_ERROR = "Data integrity error."
    INTERNAL_SERVER_ERROR = "Internal server error."


    def format(self, **kwargs):
        return HTTPMessages(self.value.format(**kwargs))