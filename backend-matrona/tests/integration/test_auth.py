#test a de intergacion a registro y login
def test_registro_admin(client):

    data = {
        "id_rol": 1,
        "nombre": "Juan",
        "apellido": "Perez",
        "correo": "cliente@test.com",
        "contrasena": "123456",
        "direccion": "Calle 1",
    }

    response = client.post("auth/registro", json=data)

    assert response.status_code == 200

    body = response.json()

    assert body["correo"] == "cliente@test.com"
    assert body["id_rol"] == 1

#test login y registro integracion
def test_login_admin(client):

    client.post("auth/registro", json={
        "nombre": "Admin",
        "apellido": "Test",
        "correo": "adminlogin@test.com",
        "contrasena": "123456",
        "direccion": "Oficina",
        "id_rol": 1
    })

    response = client.post(
        "auth/login",
        data={
            "correo": "adminlogin@test.com",
            "contrasena": "123456"
        },
        follow_redirects=False
    )

    # validar redirect
    assert response.status_code == 303

    # validar que redirige al menú admin
    assert response.headers["location"] == "/menu"

    # validar que se creó la cookie con el token
    assert "access_token" in response.cookies

#test contraseña incorrecta
def test_login_password_incorrecta(client):

    client.post("auth/registro", json={
        "nombre": "Admin",
        "apellido": "Test",
        "correo": "adminerror@test.com",
        "contrasena": "123456",
        "direccion": "Oficina",
        "id_rol": 1
    })

    response = client.post(
        "auth/login",
        data={
            "correo": "adminerror@test.com",
            "contrasena": "mala"
        },
        follow_redirects=False
    )

    assert response.status_code == 401