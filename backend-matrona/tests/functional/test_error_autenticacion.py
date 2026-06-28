import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


def test_login_fallido_muestra_mensaje_error(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://127.0.0.1:8000/")

    wait.until(EC.presence_of_element_located((By.NAME, "correo")))

    driver.find_element(By.NAME, "correo").send_keys("correo_invalido@gmail.com")
    driver.find_element(By.NAME, "contrasena").send_keys("contrasena_incorrecta")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(EC.url_contains("/error"))

    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Verifica tus datos e intenta nuevamente" in body_text
