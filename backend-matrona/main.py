from fastapi import FastAPI, HTTPException, Request, Depends
from routers.inventario import router as inventario_router
from routers.catalogo_router import router as catalogo_router
from routers.usuario import router as usuario_router
from routers import usuario_auth
from routers import cliente
from routers.pedido_router import router as pedido_router
#from routers.ws_router import router as ws_router
from routers.proveedor_router import router as proveedor_router
from routers.materiales_router import router as materiales_router
from routers.contabilidad_router import router as contabilidad_router
from routers.empleado_router import router as empleado_router
from routers.cliente import router as cliente_router
from models import Usuario, Rol, Inventario
from db import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
#from fastapi import WebSocket
#from utils.websocket import manager
from utils.deps import get_current_user




Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Matrona")

# Base del proyecto (carpeta backend-matrona)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta al frontend
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend-matrona")

# Rutas específicas
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates HTML
templates = Jinja2Templates(directory=TEMPLATES_DIR)

#ruta para mostrar el formulario
@app.get("/agregar-inventario", response_class=HTMLResponse)
async def agregar_inventario(request: Request):
    return templates.TemplateResponse("agregarInventario.html", {"request": request})

# Ruta para abrir inventario.html
@app.get("/inventario", response_class=HTMLResponse)
async def mostrar_inventario(request: Request, current_user:Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("inventario.html", {"request":request, "user_role":current_user.id_rol, "user_name":current_user.nombre})

#ruta para abrir catalogo
@app.get("/catalogo", response_class=HTMLResponse)
async def mostrar_catalogo(request: Request, current_user:Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("catalogo.html", {"request":request, "user_role": current_user.id_rol, "user_name":current_user.nombre})

#ruta para put modificar mediante el formulari
@app.get("/editar-inventario/{id_catalogo}", response_class=HTMLResponse)
async def editar_inventario(request: Request, id_catalogo: int, current_user:Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("agregarInventario.html", {
        "request": request,
        "id_catalogo": id_catalogo,
        "user_role": current_user.id_rol,
        "user_name": current_user.nombre,
        "header_title": "Modificar Cerveza",
    })
#ruta para mostrar el formulario
@app.get("/auth/registro", response_class=HTMLResponse)
def mostrar_registro(request: Request):
    return templates.TemplateResponse(request, "registrosUsuario.html", {"request": request})

#ruta para redirigir al login
@app.get("/", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse(request, "inicioSesion.html", {"request": request})

#ruta menu
@app.get("/menu")
def mostrar_menu(request: Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse(request, "menu.html", {"request": request, "user_role": current_user.id_rol, "user_name": current_user.nombre})

#ruta para mostrar proveedor
@app.get("/proveedor")
async def mostrar_proveedor(request: Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse(request, "Proveedores.html", {"request": request, "user_role": current_user.id_rol, "header_title": "Gestión Proveedores", "user_name":current_user.nombre}) #agregar getcurrent user a todos los endpoints

#ruta para Materiales
@app.get("/materiales", response_class=HTMLResponse)
async def materiales_interfaz(request: Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("Materiales.html", {"request": request, "user_role":current_user.id_rol, "user_name":current_user.nombre})
#ruta contable
@app.get("/contabilidad", response_class=HTMLResponse)
async def interfaz_contable(request: Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("contabilidad.html", {"request": request, "user_role":current_user.id_rol, "header_title": "Panel Contabilidad", "user_name":current_user.nombre})

#ruta para gestionEmpleados
@app.get("/empleados")
async def gestion_empleados(request: Request, current_user:Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("gestionEmpleados.html", {"request": request, "user_role": current_user.id_rol, "header_title": "Panel Gestión de Empleados", "user_name": current_user.nombre})

#ruta para interfaz principal empleados
@app.get("/empleados/interfaz", response_class=HTMLResponse)
async def interfaz_empleado(request: Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("empleadoInterfaz.html", {"request": request, "user_role": current_user.id_rol, "user_name":current_user.nombre})

#ruta interfazp para listar clientes
@app.get("/clientes", response_class=HTMLResponse)
async def listar_clientes(request:Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("gestionClientes.html", {"request":request, "header_title": "Panel Gestión de Clientes", "user_role": current_user.id_rol, "user_name": current_user.nombre})

#ruta interfaz pedidos cliente
@app.get("/pedidos/cliente")
async def control_pedidos(request: Request, current_user: Usuario = Depends(get_current_user)):
    return templates.TemplateResponse("pedidosCliente.html", {"request": request, "user_role": current_user.id_rol, "user_name":current_user.nombre})



app.include_router(usuario_router)
app.include_router(inventario_router)
app.include_router(catalogo_router)
app.include_router(cliente.router)
#app.include_router(ws_router)
app.include_router(usuario_auth.router)
app.include_router(pedido_router)
app.include_router(proveedor_router)
app.include_router(materiales_router)
app.include_router(contabilidad_router)
app.include_router(empleado_router)
app.include_router(cliente_router)
