El Software de gestion administrativa Matrona presenta un avance completamente funcional
Se agregaron los modulos: Autenticación de usuarios, módulo para empleados, Inventario, Catalogo, Materiales, Clientes, Pedidos, Contabilidad, proveedores.
EL sistema incluye las siguientes funcionalidades:
Usuarios: registro de usuarios segun rol Administrador/cliente/empleado, login con correo y contraseña con permisos de acuerdo al rol y token de sesion por 60 minutos.

Empleados:  empleados cuenta con su propia interfaz y funciones, ademas el administrador puede modificar datos del empleados, como area laboral, salario etc. 


Materiales: Ingreso de nuevas cervezas, editar tipo de cervezas, ver detalles de cervezas, añadir nuevas cervezas a una lista especifica y eliminar cerveza.

Catalogo: el sistema muestra al cliente todas las cervezas disponibles y permite reservar pedidos, por unidad, por caja y por sixpack. realizado el pedido se envia en tiempo real 
la notificacion con los datos del pedido a la interfaz administrador menu.

Pedidos: el sistema notifica en tiempo real el pedido reservado por medio la tegnologia WebSocket, ademas procesa los datos de cada pedido,
crucial para la informacion financiera que se mostrara en el modulo contable.

Materiales: el sistema permite llevar el control de materiales primarios para la produccion de cerveza mediante las siguientes funciones:
agregar material y cantidad segun su necesidad en la empresa; producuir/envasar,
editar el material segun su uso, o eliminarlo, mostrar todos los materiales de acuerdo al tipo de material en contenedores diferentes en la interfaz.

proveedores: Agregar proveedores con toda su informacion para tener un control de los proveedores de la empresa.

Contabilidad: el sistema muestra todo el historial de pedidos realizado, el total de ingresos y los ingresos individuales de cada cerveza, ademas incluye una grafica que facilita el análisis de datos.


En la carpeta documentos-del-proyecto se encuentra la documentacion de la fase de análisis y en la carpeta documentos-de-pruebas se encuentra la documentacion de las pruebas del Software.

