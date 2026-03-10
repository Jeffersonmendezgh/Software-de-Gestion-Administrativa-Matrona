#integracion de modulos inventario y catalogo
def test_crear_catalogo_e_inventario(client):

    response = client.post(
        "/catalogo/inventario/create/",
        json={
            "nombre_bebida": "Matrona artesanal",
            "cantidad_disponible": 50,
            "descripcion": "Cerveza de prueba",
            "contenido": 330,
            "alcohol": "6%",
            "precio_unidad": 5000,
            "precio_sixpack": 28000,
            "precio_caja": 100000
        }
    )

    assert response.status_code == 200

    data = response.json()

    # ahora verificamos que exista en inventario
    inventario = client.get("/catalogo/")

    assert inventario.status_code == 200

    lista = inventario.json()

    assert any(i["nombre_bebida"] == "IPA Test" for i in lista)

    assert data["descripcion"] == "Cerveza de prueba"
    assert data["contenido"] == 330

#test creacion de objetos en cascada

def test_crear_catalogo_e_inventario(client):

    response = client.post(
        "/catalogo/inventario/create/",
        json={
            "nombre_bebida": "MatronaTest",
            "cantidad_disponible": 50,
            "descripcion": "Cerveza de prueba",
            "contenido": 330,
            "alcohol": "6%",
            "precio_unidad": 5000,
            "precio_sixpack": 28000,
            "precio_caja": 100000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["descripcion"] == "Cerveza de prueba"

    # ahora verificamos que exista en inventario
    inventario = client.get("/catalogo/")

    assert inventario.status_code == 200

    lista = inventario.json()
    print(lista)

    assert any(i["descripcion"] == "Cerveza de prueba" for i in lista)


#test crear agregar al stock
def test_agregar_stock(client):

    client.post("/catalogo/inventario/create/", json={
        "nombre_bebida": "IPA",
        "cantidad_disponible": 10,
        "descripcion": "Test",
        "contenido": 330,
        "alcohol": "6%",
        "precio_unidad": 5000,
        "precio_sixpack": 28000,
        "precio_caja": 100000
    })

    # agregar stock
    response = client.patch("/inventario/agregar-stock/1", json={"unidades": 5})

    assert response.status_code == 200

    data = response.json()

    assert data["cantidad_disponible"] == 15