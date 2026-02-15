Estructura del Proyecto Matrona

El Software de gestión administrativa Matrona, es un sistema que busca cumplir con las necesidades tegnologícas de una empresa en crecimiento,
es por eso que su estructura ha sido cuidadosamente seleccionada pensando en construir un sistema escalable, moderno, seguro y facil de mantener.

Se desarrolla un sistema modular, el cual esta dividido en módulos para cada funcionalidad, se separa el backend de el frontend para 
mantener el orden del proyecto, siguiendo buenas practicas de programación.

A continuación se realiza un resumen de la organizacion del proyecto:
En la raiz del proyecto se encuentran los directorios para el backend y para el frontend
se crea el .gitignore, clave para evitar carga de archivos innecesarios a git, o archivos de seguridad
requirements.txt el cual contiene todas las dependencias necesarias para que el sistema funcione correctamente.
asi mismo se encuentra readme.md el cual explica la estrucutura del proyecto, y redme.txt que explica las funcionalidades del proyecto,
y su funcionamiento.

Directorio backend-matrona:
cuanta con el backend del proyecto, carpetas para utils, modelos, routers y esquemas pydantic.
archivo corazon del proyecto: main.py gestiona todo el sistema mediante los routers,
archivos con variables de entorno y configuracion de la coneccion de la base de datos.
Separación de responsabilidades, cada funcionalidad cuenta con su modelo de datos, clases con responsabilidades unicas y routers
exclusivamente para su funcionalidad, cumpliendo principios como responsabilidades unicas.

Directorio Frontend Matrona
este carpeta tiene toda la estructura del proyecto, separada del backend, hace facil su mantenimiento, y permite
el crecimiento del sistema de manera escalable.
Contiene directorio static, para los archivos estaticos, en este caso archivos JavaScript.
Templates: contiene las plantillas HTML y estilos Tailwind css, cada plantilla esta vincualada correctamente a su archivo js.
El tener un archivo js unico para cada funcionalidad y su HTMl correspondiente separado, permite una mayor flexibilidad, deteccion de errores,
y hace el sistema mucho mas facil de mantener. cada JS se encarga de realizar el fetch a nuestra API en FastAPI 
procesar los datos que llegan, y renderizar cada plantilla HTML con los datos que van llegando del backend, esto en caso de solicitudes get,
Para solicitudes POST, PATH, PUT, mayoritariamente mediante funciones JavaScript, nos encargamos de campturar los datos de los inputs, procesarlos y
enviarlos al backend en formato JSON.



Como se puede ver el Software de Gestión Administrativa Matrona mantiene una organización módular, se promueve la separación de responsabilidades,
la reutilizacion de codigo y la seguridad mediante autenticación JWT, logrando asi un sistema robusco y facil de escalar.


