El Software de gestion administrativa Matrona presenta un avance completamente funcional en sus modulos principales
Usuarios, Inventario catalogo y pedidos. Se han realizado ajustes al sistema de roles administrador y cliente.
para inicializar el software es importante tener su entorno virtual activado: .\venv\Scripts\activate es necesario activarlo en la raiz del proyecto.
navegar hasta la carpeta backend-matrona: cd backend-matrona: 
ejecutar el servidor: uvicorn main:app --reload. se requiere moverse a la carpeta backend-matrona para poder ejecutar el servidor, ya que el path esta configurado mediante main:app 
una vez ejecutado el servidor se puede probar cualquera de las rutas que se presentan a continuacion:
http://127.0.0.1:8000/docs  documentacion de todas las apis del proyecto, es la ruta mas importante ya que alli estan todas las rutas que he creado y su documentacion
http://127.0.0.1:8000/inventario  muestra el inventario
http://127.0.0.1:8000/inventario/ muestra los archivos JSON del inventario
http://127.0.0.1:8000/catalogo muestra el catalogo
http://127.0.0.1:8000/auth/registro lleva al formulario de registro
http://127.0.0.1:8000/auth/login lleva al inicio de sesion 
http://127.0.0.1:8000/usuarios get que muestra todos los usuarios en JSON

se pueden encontrar cada una de estas rutas en la swegger de FastAPI en donde ademas se podran probar de manera similar a POSTMAN

Se ha terminado el modulo de pedidos presentando una funcionalidad completa.
solo el usuario logeado con rol cliente podra reservar pedidos desde el Catalogo.
Las notificaciones del pedido se envian en tiempo real a la interfaz menu administrador