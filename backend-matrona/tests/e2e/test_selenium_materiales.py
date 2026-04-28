from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time

def test_agregar_material():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000") 

    # Login
    driver.find_element(By.NAME, "correo").send_keys("jefferson18.estudios@gmail.com")
    driver.find_element(By.NAME, "contrasena").send_keys("12345")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(2)

    # id materiales
    driver.get("http://localhost:8000/materiales") 

    time.sleep(2)

    # materiales a agregar
    driver.find_element(By.ID, "tipoMaterial").send_keys("Lúpulo")
    driver.find_element(By.ID, "cantidadAgregar").send_keys("50")

    # Submit para agregar el material a la db
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(2)

    # Validacion
    tabla = driver.find_element(By.CSS_SELECTOR, "#tabla-produccion tbody")
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    assert any("Lúpulo" in fila.text for fila in filas)
    # Buscar la fila que contiene "Lúpulo"
    fila_objetivo = None
    for fila in filas:
        if "Lúpulo" in fila.text:
            fila_objetivo = fila
            break

    assert fila_objetivo is not None

    # Click en el botón eliminar dentro de esa fila
    boton_eliminar = fila_objetivo.find_element(By.CLASS_NAME, "eliminar-btn")
    boton_eliminar.click()
    #Manejar la alerta, osea aceptar para elimar
    alerta = driver.switch_to.alert
    alerta.accept()     # confirma

    time.sleep(2)

    # Validar que el material ya no existe en la tabla
    tabla = driver.find_element(By.CSS_SELECTOR, "#tabla-produccion tbody")
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    assert not any("Lúpulo" in fila.text for fila in filas)

    driver.quit()