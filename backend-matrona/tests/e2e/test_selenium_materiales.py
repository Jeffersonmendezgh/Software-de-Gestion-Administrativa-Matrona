from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

    driver.quit()