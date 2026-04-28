def test_entregar_pedido_y_descuento_inventario(client):

    #  Registrar usuario cliente
    client.post("/auth/registro", json={
        "nombre": "Cliente",
        "apellido": "Test",
        "correo": "cliente@test.com",
        "contrasena": "123456",
        "direccion": "Casa",
        "id_rol": 3
    })

    #  Login 
    response_login = client.post(
        "/auth/login",
        data={
            "correo": "cliente@test.com",
            "contrasena": "123456"
        },
        follow_redirects=False
    )

    assert response_login.status_code == 303
    assert "access_token" in response_login.cookies


    # Crear cerveza inventario  catálogo
    client.post("/catalogo/inventario/create/", json={
        "nombre_bebida": "IPA",
        "cantidad_disponible": 100,
        "descripcion": "Cerveza test",
        "contenido": 330,
        "alcohol": "6%",
        "precio_unidad": 5000,
        "precio_sixpack": 28000,
        "precio_caja": 100000
    })

    # Crear pedido, ya autenticado por cookie
    response_pedido = client.post("/pedidos/", json={
        "items": [
            {
                "id_catalogo": 1,
                "cantidad_pedido_uds": 10,
                "presentacion": "unidad"
            }
        ]
    })

    assert response_pedido.status_code == 201

    pedido_id = response_pedido.json().get("id_pedidos", 1)

    # Entregar pedido
    response = client.put(f"/pedidos/{pedido_id}/estado")

    assert response.status_code == 200
    assert response.json()["estado"] == "entregado"

    #Validar inventario actualizado
    response_inventario = client.get("/inventario/1")

    assert response_inventario.status_code == 200
    assert response_inventario.json()["cantidad_disponible"] == 90