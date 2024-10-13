import json
from datetime import datetime
from typing import Any


def json_serialize(data: Any) -> str:
    """
    Serializes Python objects to a JSON-formatted string, with special handling for datetime objects.

    Args:
        data (Any): The Python object to serialize.

    Returns:
        str: A JSON-formatted string.
    """

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime objects to ISO format
            # Add more custom serialization rules here if needed
            return json.JSONEncoder.default(self, obj)

    return json.dumps(data, cls=CustomEncoder)
