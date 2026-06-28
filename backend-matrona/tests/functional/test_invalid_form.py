import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


def test_formulario_proveedor_no_envia_si_esta_vacio(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://127.0.0.1:8000/")

    wait.until(EC.visibility_of_element_located((By.ID, "correoLogin")))
    correo_input = driver.find_element(By.ID, "correoLogin")
    contrasena_input = driver.find_element(By.ID, "contrasenaLogin")

    correo_input.clear()
    correo_input.send_keys("jefferson18.estudios@gmail.com")
    contrasena_input.clear()
    contrasena_input.send_keys("12345")
    driver.find_element(By.ID, "btnIniciarSesion").click()

    wait.until(lambda d: d.current_url != "http://127.0.0.1:8000/")

    driver.get("http://127.0.0.1:8000/proveedor")

    wait.until(EC.presence_of_element_located((By.ID, "formularioProveedor")))

    driver.find_element(By.ID, "btn-agregarProveedor").click()

    try:
        mensaje_error = wait.until(EC.visibility_of_element_located((By.ID, "mensajeError")))
        assert "Completa todos los campos" in mensaje_error.text
    except TimeoutException:
        assert driver.find_element(By.ID, "formularioProveedor").is_displayed()
