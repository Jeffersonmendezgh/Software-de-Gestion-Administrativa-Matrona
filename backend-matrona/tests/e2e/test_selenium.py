from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_abrir_navegador():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("http://127.0.0.1:8000")  # app corriendo

    time.sleep(5) # delay para ver la pagina sino se me cierra muy rapido

    assert "Autenticación Matrona" in driver.title

    driver.quit()