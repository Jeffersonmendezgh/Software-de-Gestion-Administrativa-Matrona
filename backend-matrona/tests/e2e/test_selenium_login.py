from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_selenium():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("http://127.0.0.1:8000")

    # esperar input correo
    WebDriverWait(driver, 10).until(#tiempo maximo de espera dirver, 10
        EC.presence_of_element_located((By.NAME, "correo"))
    )

    driver.find_element(By.NAME, "correo").send_keys("jefferson18.estudios@gmail.com")
    driver.find_element(By.NAME, "contrasena").send_keys("12345")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # esperar redirección
    WebDriverWait(driver, 10).until(
        EC.url_contains("/menu")
    )

    assert "/menu" in driver.current_url

  
    driver.quit()