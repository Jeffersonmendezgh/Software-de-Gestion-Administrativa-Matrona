from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_usuario_existente():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        #  Ir al login
        driver.get("https://matrona-service.onrender.com/")

        #  Esperar formulario de login
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        # 3. Ingresar credenciales (usa el mismo usuario que registraste)
        driver.find_element(By.NAME, "correo").send_keys("jefferson18.estudios@gmail.com")  # cámbialo si usaste dinámico
        driver.find_element(By.NAME, "contrasena").send_keys("12345")

        # Enviar formulario
        driver.find_element(By.TAG_NAME, "form").submit()

        
        try:
            wait.until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print("ALERTA LOGIN:", alert.text)
            alert.accept()
        except:
            print("Login sin alertas")

        #  Validar acceso al sistema
        wait.until(EC.url_contains("menu"))

        assert "menu" in driver.current_url

    finally:
        driver.quit()