def test_flujo_inventario_completo(client):

    # crear cerveza
    client.post("/catalogo/inventario/create/", json={
        "nombre_bebida": "IPA Flujo",
        "cantidad_disponible": 10,
        "descripcion": "Test",
        "contenido": 330,
        "alcohol": "6%",
        "precio_unidad": 5000,
        "precio_sixpack": 28000,
        "precio_caja": 100000
    })

    # agregar stock
    client.patch("/inventario/agregar-stock/1", json={"unidades": 5})

    # consultar inventario
    response = client.get("/catalogo/")

    inventario = response.json()

    assert any(i["inventario"]["cantidad_disponible"] == 15 for i in inventario)

# este test tiene el objetivo de proar funcionalidad completa desde que el usuario ingresa al sistema
#hasta que se actualize el stock para finalmente obtener el catalogo actualizado
def test_flujo_completo_inventario(client):

    # registrar administrador
    registro = client.post("auth/registro", json={
        "id_rol": 1,
        "nombre": "Admin",
        "apellido": "Inventario",
        "correo": "admininventario@test.com",
        "contrasena": "123456",
        "direccion": "Oficina",
    })

    assert registro.status_code == 200

    #  login
    login = client.post(
        "auth/login",
        data={
            "correo": "admininventario@test.com",
            "contrasena": "123456"
        },
        follow_redirects=False
    )

    assert login.status_code == 303
    assert "access_token" in login.cookies

    cookies = login.cookies

    #  crear cerveza
    crear = client.post(
        "/catalogo/inventario/create/",
        json={
            "nombre_bebida": "matrona artesanal",
            "cantidad_disponible": 10,
            "descripcion": "Cerveza artesanal",
            "contenido": 330,
            "alcohol": "6%",
            "precio_unidad": 5000,
            "precio_sixpack": 28000,
            "precio_caja": 100000
        },
        cookies=cookies
    )

    assert crear.status_code == 200

    #  agregar stock
    stock = client.patch(
        "/inventario/agregar-stock/1",
        json={"unidades": 5},
        cookies=cookies
    )

    assert stock.status_code == 200

    #  consultar catálogo
    catalogo = client.get("/catalogo/", cookies=cookies)

    assert catalogo.status_code == 200

    lista = catalogo.json()

    # verificar que la cerveza exista
    cerveza = next(
        (c for c in lista if c["inventario"]["nombre_bebida"] == "matrona artesanal"),
        None
    )

    assert cerveza is not None

    # verificar stock actualizado
    assert cerveza["inventario"]["cantidad_disponible"] == 15