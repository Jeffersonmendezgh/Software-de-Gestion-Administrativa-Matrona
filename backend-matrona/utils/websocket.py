from typing import List
from fastapi import WebSocket
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.loop = None  # guardaremos el loop principal aquí

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_json(self, message: dict):
        data = json.dumps(message)
        for connection in list(self.active_connections):
            try:
                await connection.send_text(data)
            except Exception:
                self.disconnect(connection)

    def broadcast_json_sync(self, message: dict):
        """
        Llamable desde BackgroundTasks, aunque esté en un worker thread por ahora lo manejare asi.
        """
        if not self.loop:
            raise RuntimeError(" No se inicializó el loop principal")

        # Programar la tarea en el loop principal desde otro hilo
        self.loop.call_soon_threadsafe(
            asyncio.create_task, self.broadcast_json(message)
        )

manager = ConnectionManager()
