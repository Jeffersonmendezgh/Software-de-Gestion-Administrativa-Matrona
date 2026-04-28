def test_crear_proveedor(client):

    #  Registrar admin
    client.post("auth/registro", json={
        "nombre": "Admin",
        "apellido": "Test",
        "correo": "adminproveedor@test.com",
        "contrasena": "123456",
        "direccion": "Oficina",
        "id_rol": 1
    })

    #  Login
    response_login = client.post(
        "auth/login",
        data={
            "correo": "adminproveedor@test.com",
            "contrasena": "123456"
        },
        follow_redirects=False
    )

    assert response_login.status_code == 303

    # Guardar cookies en el cliente
    client.cookies.update(response_login.cookies)

    # test
    response = client.post(
        "/proveedor/",
        json={
            "nombre_proveedor": "Proveedor Lúpulo",
            "material_que_provee": "Lúpulo",
            "cantidadM": "100",
            "telefono": "3001234567",
            "direccion_proveedor": "Cúcuta",
            "frecuencia_entrega": "Semanal"
        }
    )

    #  Validaciones
    assert response.status_code == 201

    data = response.json()

    assert data["nombre_proveedor"] == "Proveedor Lúpulo"
    assert data["material_que_provee"] == "Lúpulo"
    assert data["cantidadM"] == "100"