import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


#  fixture driver
@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


#  test solicitar cotizacion
def test_solicitar_cotizacion(driver):
    wait = WebDriverWait(driver, 10)

    #  abrir app
    driver.get("http://127.0.0.1:8000")

    #  login
    wait.until(EC.presence_of_element_located((By.NAME, "correo")))

    driver.find_element(By.NAME, "correo").send_keys("agustin@gmail.com")
    driver.find_element(By.NAME, "contrasena").send_keys("12345")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # esperar cambio de URL 
    wait.until(lambda d: d.current_url != "http://127.0.0.1:8000/")

    print("URL después del login:", driver.current_url)

    # asegurar token en localStorage 
    driver.execute_script("""
        if (!localStorage.getItem('token')) {
            localStorage.setItem('token', 'token_test');
        }
    """)

    #  ir a catalogo
    driver.get("http://127.0.0.1:8000/catalogo")

    # esperar render dinámico del catálogo
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-id]")))

    #  seleccionar producto
    card = driver.find_elements(By.CSS_SELECTOR, "[data-id]")[0]

    # seleccionar presentación
    select_element = card.find_element(By.CLASS_NAME, "presentacion")
    Select(select_element).select_by_value("sixpack")

    # ingresar cantidad
    input_cantidad = card.find_element(By.CLASS_NAME, "cantidad")
    input_cantidad.clear()
    input_cantidad.send_keys("6")

    # hacer cotizacion 
    boton_cotizar = card.find_element(By.CLASS_NAME, "btn-cotizar")
    driver.execute_script("arguments[0].click();", boton_cotizar)

    # esperar a que aparezca el modal de cotización y su contenido
    wait.until(lambda d: "hidden" not in d.find_element(By.ID, "modal-cotizacion").get_attribute("class"))
    wait.until(lambda d: d.find_element(By.ID, "contenido-cotizacion").text.strip() != "")

    # validar contenido generado
    contenido = driver.find_element(By.ID, "contenido-cotizacion")
    assert "Cotización" in contenido.text or "Total" in contenido.text

    time.sleep(2)