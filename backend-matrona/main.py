from fastapi import FastAPI, HTTPException, Request
from routers.inventario import router as inventario_router
from routers.catalogo_router import router as catalogo_router
from routers.usuario import router as usuario_router
from routers import usuario_auth
from routers import cliente
from routers.pedido_router import router as pedido_router
from routers.ws_router import router as ws_router
from models import Usuario, Rol, Inventario
from db import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import WebSocket
from utils.websoket import manager
import models



Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Matrona")

#  Ruta absoluta de la carpeta frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend-matrona")

# Servir la carpeta frontend como "static"

#  Base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a la carpeta "static" dentro de frontend-matrona
static_path = os.path.join(BASE_DIR, "..", "frontend-matrona", "static")

# Montar la carpeta estática
app.mount("/static", StaticFiles(directory="../frontend-matrona/static"), name="static")
#templates HTML
templates = Jinja2Templates(directory="../frontend-matrona/templates")

#ruta para mostrar el formulario
@app.get("/agregar-inventario", response_class=HTMLResponse)
async def agregar_inventario(request: Request):
    return templates.TemplateResponse("agregarInventario.html", {"request": request})

# Ruta para abrir inventario.html
@app.get("/inventario", response_class=HTMLResponse)
async def mostrar_inventario(request: Request):
    return templates.TemplateResponse("inventario.html", {"request":request})

#ruta para abrir catalogo
@app.get("/catalogo", response_class=HTMLResponse)
async def mostrar_catalogo(request: Request):
    return templates.TemplateResponse("catalogo.html", {"request":request})

#ruta para put modificar mediante el formulari
@app.get("/editar-inventario/{id_catalogo}", response_class=HTMLResponse)
async def editar_inventario(request: Request, id_catalogo: int):
    return templates.TemplateResponse("agregarInventario.html", {
        "request": request,
        "id_catalogo": id_catalogo
    })
#ruta para mostrar el formulario
@app.get("/auth/registro", response_class=HTMLResponse)
def mostrar_registro(request: Request):
    return templates.TemplateResponse("registrosUsuario.html", {"request": request})

#ruta para redirigir al login
@app.get("/auth/login", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse("inicioSesion.html", {"request": request})

#ruta menu
@app.get("/menu")
def mostrar_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


app.include_router(usuario_router)
app.include_router(inventario_router)
app.include_router(catalogo_router)
app.include_router(cliente.router)
app.include_router(ws_router)
app.include_router(usuario_auth.router)
app.include_router(pedido_router)

