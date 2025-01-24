from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# Manager to handle active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()  # Accept the WebSocket connection
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message_to_all(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await manager.connect(websocket)  # Add the connection
    try:
        while True:
            data = await websocket.receive_text()  # Receive message from client
            await manager.send_message_to_all(data)  # Broadcast to all clients
    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Remove connection when client disconnects
