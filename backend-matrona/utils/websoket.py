#Los WebSockets permiten comunicación bidireccional en tiempo real entre el cliente y el servidor. A diferencia de HTTP (que es request-response),
#  los WebSockets mantienen una conexión persistente
from typing import List
from fastapi import WebSocket
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(WebSocket)

    def disconect(self, websocket: WebSocket):
            if websocket in self.active_connections:
                  self.active_connections.remove(websocket)

    async def broadcast_json(self, message: dict):
          data = json.dumps(message)
          #para enviar a todas las conecxiones
          for connection in list(self.active_connections):
                try:
                    await connection.send_text(data)
                except Exception:
                    self.disconect(connection)

    #helper para programar desde Bacgoundtaks (no await)
    def broadcast_json_sync(self, message: dict):
          #programa la tarea asicrona el el loop actual
        asyncio.run(self.broadcast_json(message))

manager = ConnectionManager()                
    