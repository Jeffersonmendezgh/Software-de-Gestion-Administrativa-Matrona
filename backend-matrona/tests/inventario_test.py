#probar get inventario
def test_listar_inventario(client):
    response = client.get("/inventario/")
    assert response.status_code == 200

#agregar stock
def test_agregar_stock(client):
    response = client.patch("/inventario/agregar-stock/1", json={"unidades": 5})
    