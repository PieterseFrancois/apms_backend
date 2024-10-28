from fastapi import WebSocket
from typing import Dict

from app.utils.json_utils import json_serialize
from app.utils.message_identifiers import MessageIdentifiers


class ConnectionManager:
    def __init__(self):
        # Dictionary to store active WebSocket connections by client_id
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """
        Accepts and stores a new WebSocket connection for a given client identifier.

        Args:
            websocket (WebSocket): The WebSocket connection.
            client_id (str): The client identifier.
        """
        client_id = str(client_id)
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        print(f"Client {client_id} connected. Total connections: {len(self.active_connections[client_id])}")


    def disconnect(self, client_id: str, websocket: WebSocket) -> None:
        """
        Removes and closes a WebSocket connection by client identifier.

        Args:
            client_id (str): The client identifier.
        """
        client_id = str(client_id)
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            print(f"Client {client_id} disconnected. Remaining connections: {len(self.active_connections[client_id])}")
            if not self.active_connections[client_id]:  # If no more connections, remove the client_id entry
                del self.active_connections[client_id]

    async def send_personal_message(
        self, message: any, client_id: str, identifier: MessageIdentifiers
    ) -> None:
        """
        Sends a personal message to a specific client by client identifier.

        Args:
            message (any): The message to send.
            client_id (str): The client identifier.
            identifier (MessageIdentifiers): The message identifier.
        """
        # Add the identifier to the message
        message = json_serialize({"identifier": identifier.value, "message": message})
        client_id = str(client_id)

        if client_id in self.active_connections:
            for websocket in self.active_connections[client_id]:
                await websocket.send_text(message)
                print(f"Message sent to client {client_id}")

    async def broadcast(self, message: any, identifier: MessageIdentifiers) -> None:
        """
        Broadcasts a message to all connected clients.

        Args:
            message (str): The message to broadcast.
            identifier (MessageIdentifiers): The message identifier.
        """

        # Add the identifier to the message
        message["identifier"] = identifier.value

        message = json_serialize(message)

        for client_id, websockets in self.active_connections.items():
            for websocket in websockets:
                await websocket.send_text(message)
                print(f"Broadcast message to client {client_id}")


# Create a global instance of the connection manager
manager = ConnectionManager()
