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


#  test pedido cliente
def test_realizar_pedido_cliente(driver):
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
    input_cantidad.send_keys("1")

    #  hacer pedido
    boton_reservar = driver.find_element(By.CLASS_NAME, "btn-reservar")
    driver.execute_script("arguments[0].click();", boton_reservar)

    # validar alerta
    wait.until(
        lambda d: len(d.find_element(By.ID, "alerta").text.strip()) > 0
    )

    alerta = driver.find_element(By.ID, "alerta")

    assert alerta.text.strip() != ""

    print("Mensaje de alerta:", alerta.text)

    time.sleep(3)
