#este test evalua la funcionalidad complete de registro y login con token de acceso y redireccion
def test_flujo_completo_autenticacion(client):
    registro = client.post("auth/registro", json={
        "nombre": "Admin",
        "apellido": "Flujo",
        "correo": "flujo@test.com",
        "contrasena": "123456",
        "direccion": "Oficina",
        "id_rol": 1
    })

    assert registro.status_code == 200

    #  login
    login = client.post(
        "auth/login",
        data={
            "correo": "flujo@test.com",
            "contrasena": "123456"
        },
        follow_redirects=False
    )

    assert login.status_code == 303

    # revisamos si esta el token en la cookie
    assert "access_token" in login.cookies

    # guardar cookie
    cookies = login.cookies

    # entramos a la pagina protegida, y claro tenemos que pasarle la cookie para poder acceder al sistema
    menu = client.get("/menu", cookies=cookies)

    assert menu.status_code == 200