# routers/ws_router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.websocket import manager   # coincide con el nombre del fichero arriba

router = APIRouter()

@router.websocket("/ws/pedidos")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
