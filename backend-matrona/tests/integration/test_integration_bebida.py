def test_agregar_producto_y_ver_catalogo(client):
    # 1. Crear producto
    response = client.post("/catalogo/inventario/create/", json={
        "nombre_bebida": "Matrona artesanal",
        "cantidad_disponible": 50,
        "descripcion": "Cerveza de prueba",
        "contenido": 330,
        "alcohol": "6%",
        "precio_unidad": 5000,
        "precio_sixpack": 28000,
        "precio_caja": 100000
    })
    assert response.status_code == 200

    
    #  Consultar catálogo
    response = client.get("/catalogo/")
    data = response.json()

    #  Extraer nombres correctamente para verificar actualizacion
    # es json anidado por lo cual hay que acceder asi
    nombres = [p["inventario"]["nombre_bebida"] for p in data]

    # 4. Validar que existe
    assert "Matrona artesanal" in nombres