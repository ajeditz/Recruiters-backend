from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{room_id}/{user_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()  # Expecting JSON data
            message = {
                "user_id": user_id,
                "room_id": room_id,
                "content": data["message"],  # Message text
            }
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        disconnect_message = {"user_id": user_id, "room_id": room_id, "content": "User disconnected"}
        await manager.broadcast(disconnect_message)
