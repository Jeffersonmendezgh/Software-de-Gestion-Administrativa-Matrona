def test_crear_catalogo(client):

    data = {
        "nombre_bebida": "Matrona artesanal",
        "cantidad_disponible": 100,
        "descripcion": "Cerveza artesanal IPA",
        "contenido": 330,
        "alcohol": "6.5",
        "precio_unidad": 5000,
        "precio_sixpack": 28000,
        "precio_caja": 100000
    }

    response = client.post("/catalogo/inventario/create/", json=data)

    assert response.status_code == 200

    

    result = response.json()

    assert result["descripcion"] == "Cerveza artesanal IPA"


def test_obtener_catalogo(client):
    response = client.get("/catalogo/")

    assert response.status_code == 200

def test_crear_catalogo_e_inventario(client):

    response = client.post(
        "/catalogo/inventario/create/",
        json={
            "nombre_bebida": "IPA Test",
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
    inventario = client.get("/catalogo")

    assert inventario.status_code == 200

    lista = inventario.json()

    assert any(i["nombre_bebida"] == "IPA Test" for i in lista)


