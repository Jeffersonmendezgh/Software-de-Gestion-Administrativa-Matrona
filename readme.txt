El Software de gestion administrativa Matrona presenta un avance completamente funcional en sus modulos principales
Usuarios, Inventario y catalogo
para inicializar el software es importante tener su entorno virtual activado: .\venv\Scripts\activate
navegar hasta la carpeta backend-matrona: cd backend-matrona: 
ejecutar el servidor: uvicorn main:app --reload
una vez ejecutado el servidor se puede probar cualquera de las rutas que se presentan a continuacion:
http://127.0.0.1:8000/docs  documentacion de todas las apis del proyecto, es la ruta mas importante ya que alli estan todas las rutas que he creado y su documentacion
http://127.0.0.1:8000/inventario  muestra el inventario
http://127.0.0.1:8000/inventario/ muestra los archivos JSON del inventario
http://127.0.0.1:8000/catalogo muestra el catalogo
http://127.0.0.1:8000/auth/registro lleva al formulario de registro
http://127.0.0.1:8000/auth/login lleva al inicio de sesion 
http://127.0.0.1:8000/usuarios get que muestra todos los usuarios en JSON
se pueden encontrar cada una de estas rutas en la swegger de FastAPI en donde ademas se podran probar de manera similar a POSTMAN

Los modulos de pedidos son modulos en construccion, no estan terminados pero no afectan el funcionamiento de los demas modulos del sistema