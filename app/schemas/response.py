from typing import Union
from pydantic import BaseModel
from app.utils.http_messages import HTTPMessages

class Response(BaseModel):
    """
    Represents the response data for an API request.

    Attributes:
        success (bool): Indicates the success status of the API response.
        msg (HTTPMessages): The HTTP message associated with the API response.
        data (Union[
            list[],
        ]): The list of data returned by the API response.

    """

    success: bool
    msg: HTTPMessages
    data: Union[
        list[int],
    ]