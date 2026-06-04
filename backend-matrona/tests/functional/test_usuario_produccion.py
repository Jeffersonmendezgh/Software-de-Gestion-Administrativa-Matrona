from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_flujo_autenticacion_selenium():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Ir al login
        driver.get("https://matrona-service.onrender.com/")

        #  Click en registrarse
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Registrarse"))).click()

        #  Esperar formulario
        wait.until(EC.presence_of_element_located((By.ID, "formRegistro")))

        # Llenar formulario
        driver.find_element(By.ID, "nombre").send_keys("Admin")
        driver.find_element(By.ID, "apellidos").send_keys("Flujo")

        correo = f"flujo{int(time.time())}@test.com"
        driver.find_element(By.ID, "correo").send_keys(correo)

        driver.find_element(By.ID, "direccion").send_keys("Oficina")
        driver.find_element(By.ID, "contrasena").send_keys("123456")

        # seleccionar rol
        driver.find_element(By.ID, "rol").send_keys("Administrador")

        # enviar formulario
        driver.find_element(By.ID, "formRegistro").submit()

      

    finally:
        driver.quit()