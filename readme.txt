El Software de gestion administrativa Matrona presenta un avance completamente funcional
Se agregaron los modulos: Usuarios, Inventario, Catalogo, Materiales, Clientes, Pedidos, Contabilidad y proveedores.
EL sistema incluye las siguientes funcionalidades:
Usuarios: registro de usuarios segun rol Administrador/cliente, login con correo y contraseña con permisos de acuerdo al rol

Materiales: Ingreso de nuevas cervezas, editar tipo de cervezas, ver detalles de cervezas, añadir nuevas cervezas a una lista especifica y eliminar cerveza

Catalogo: el sistema muestra al cliente todas las cervezas disponibles y permite reservar pedidos, por unidad, por caja y por sixpack. realizado el pedido se envia en tiempo real 
la notificacion con los datos del pedido a la interfaz administrador menu.

Pedidos: el sistema notifica en tiempo real el pedido reservado por medio la tegnologia WebSocket, ademas procesa los datos de cada pedido,
crucial para la informacion financiera que se mostrara en el modulo contable.

ateriales: el sistema permite llevar el control de materiales primarios para la produccion de cerveza mediante las siguientes funciones:
agregar material y cantidad segun su necesidad en la empresa; producuir/envasar,
editar el material segun su uso, o eliminarlo, mostrar todos los materiales de acuerdo al tipo de material en contenedores diferentes en la interfaz.

proveedores: Agregar proveedores con toda su informacion para tener un control de los proveedores de la empresa.

Contabilidad: el sistema muestra todo el historial de pedidos realizado, el total de ingresos y los ingresos individuales de cada cerveza.

Se logra un avance sistematico en la mayoria de las funcionalidades, utilizando casos de uso, historia de usuario, trabando en todo tipo de detalle para perfeccionar el sistema de acuerdo a los requerimientos.

para ver la lista completa de rutas y schemas en FastAPI ejecutar el link: http://127.0.0.1:8000/docs o la direccion del servidor locar correspondiente
alli se presenta la documentacion api completa del sistema muy detallada gracias a FastAPI.