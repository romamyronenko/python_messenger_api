from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.chat_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, chat_id: int, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.chat_connections:
            self.chat_connections[chat_id] = []
        self.chat_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket):
        if chat_id in self.chat_connections:
            self.chat_connections[chat_id].remove(websocket)
            if not self.chat_connections[chat_id]:
                del self.chat_connections[chat_id]

    async def broadcast(self, chat_id: int, message: str):
        for connection in self.chat_connections.get(chat_id, []):
            await connection.send_text(message)

manager = ConnectionManager()
