from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

router = APIRouter()

# Lista de conexiones activas
conexiones: list[WebSocket] = []

@router.websocket("/ws/pedidos")
async def websocket_pedidos(ws: WebSocket):
    await ws.accept()
    conexiones.append(ws)
    try:
        while True:
            await ws.receive_text()  #no lo usamos pero evita cerrar la conexión por ahora
    except WebSocketDisconnect:
        conexiones.remove(ws)
