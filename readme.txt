Software de gestion administrativa Matrona 


Módulos: Usuarios, Inventario, Catalogo, Materiales, Clientes, Pedidos, Contabilidad, Proveedores, Empleados.

EL sistema incluye las siguientes funcionalidades:
Usuarios y Roles: registro de usuarios segun rol Administrador/cliente/empleado, login con correo y contraseña con permisos de acuerdo al rol y token JWT de sesion por 60 minutos.


Inventario: Ingreso de nuevas cervezas al inventario, editar tipo de cervezas, agregar al stock, ver detalles de cervezas, añadir nuevas cervezas a una lista especifica y eliminar cerveza.

Catalogo: el sistema muestra al cliente todas las cervezas disponibles y permite reservar pedidos, por unidad, por caja y por sixpack. realizado el pedido se envia en tiempo real 
la notificacion con los datos del pedido a la interfaz administrador "menu".

Pedidos: El sistema reserva el pedido el cual quedara vinculado al cliente que lo reservo, y todos los datos quedaran almacenados para el historial,

Entrega de Pedidos: solo el administrador puede cambiar el estado del pedido a entregado, el sistema restara de manera correcta las bebidas del inventario y gurdandara el 
historia de cada venta.

Contabilidad: el sistema muestra todo el historial de pedidos realizado, el total de ingresos y los ingresos individuales de cada cerveza,
además incluye una gráfica que facilita el análisis de datos.

Materiales: el sistema permite llevar el control de materiales primarios para la produccion de cerveza mediante las siguientes funciones:
agregar material y cantidad segun su necesidad en la empresa; producuir/envasar,
editar el material segun su uso, o eliminarlo, mostrar todos los materiales de acuerdo al tipo de material en contenedores diferentes en la interfaz.

proveedores: El administrador y empleado pueden agregar proveedores con toda su informacion para tener un control y mejor gestión en la empresa.

Empleados:  empleados cuenta con su propia interfaz y funciones, ademas el administrador puede modificar datos del empleados, como area laboral, salario etc. 

Flujo del sisema:
Un usuario se registra en el sistema con sus datos y el rol, posteriormente puede ingresar a el mediante correo y contraseña,
dentro del sistema el usuario puede navegar por las funciones que le permita su rol.


Link del proyecto en producción: https://matrona-service.onrender.com/
datos demo para administrador:
correo admindemo@gmail.com
contraseña:admindemo

nota: el demo esta desplegado en un servidor gratuito en render, por lo cual puede tardar hasta 50 segundos antes de iniciar, seguidamente se puede explorar el sistema con normalidad.
