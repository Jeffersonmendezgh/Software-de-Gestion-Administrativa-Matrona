#este test tiene como objetivo verificar la funcionalidad completa
#desde la creacion del pedido del admin hasta la solicitud del pedido del cliente.

def test_flujo_crear_pedido(client):

    # cliente agraga producto

    client.post("/registro", json={
        "id_rol": 1,
        "nombre": "Admin",
        "apellido": "Test",
        "correo": "admin@test.com",
        "contrasena": "123456",
        "direccion": "Oficina",
    })

    login_admin = client.post(
        "auth/login",
        data={"correo": "admin@test.com", "contrasena": "123456"},
        follow_redirects=False
    )

    admin_cookies = login_admin.cookies

    crear_producto = client.post(
        "/catalogo/inventario/create/",
        json={
            "nombre_bebida": "IPA Pedido",
            "cantidad_disponible": 20,
            "descripcion": "Cerveza test pedido",
            "contenido": 330,
            "alcohol": "6%",
            "precio_unidad": 5000,
            "precio_sixpack": 28000,
            "precio_caja": 100000
        },
        cookies=admin_cookies
    )

    assert crear_producto.status_code == 200

    # cliente se registra

    client.post("auth/registro", json={
        "id_rol": 3,
        "nombre": "Cliente",
        "apellido": "Compra",
        "correo": "cliente@test.com",
        "contrasena": "123456",
        "direccion": "Casa",
        
    })

    login_cliente = client.post(
        "auth/login",
        data={"correo": "cliente@test.com", "contrasena": "123456"},
        follow_redirects=False
    )

    cliente_cookies = login_cliente.cookies

    # cliente crea pedido

    pedido = client.post(
        "/pedidos/",
        json={
            "items": [
                {
                    "id_catalogo": 1,
                    "cantidad_pedido_uds": 2,
                    "presentacion": "unidad"
                }
            ]
        },
        cookies=cliente_cookies
    )

    assert pedido.status_code == 201

    data = pedido.json()

    # verificar total
    assert float(data["total_pedido"]) == 10000.0

    # verificar que tenga detalles
    assert len(data["detalles"]) > 0