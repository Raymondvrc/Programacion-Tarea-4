import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def test_failed_login_attempts():
    # Configuración de opciones para simular un navegador real
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Inicializar el WebDriver con las opciones
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.amazon.com/ap/signin")
    driver.maximize_window()

    max_attempts = 5
    attempt = 0
    
    try:
        while attempt < max_attempts:
            # Intentar iniciar sesión con credenciales incorrectas
            email = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_email")))
            email.clear()
            email.send_keys("invalid_email@example.com")
            
            continue_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "continue")))
            continue_button.click()

            password = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_password")))
            password.clear()
            password.send_keys("incorrect_password")
            
            sign_in_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "signInSubmit")))
            sign_in_button.click()

            # Verificar si aparece el mensaje de error de correo o contraseña incorrecta
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'There was a problem. Your password is incorrect')]"))
            )
            assert "There was a problem. Your password is incorrect" in error_message.text
            print(f"Intento fallido {attempt + 1} de {max_attempts}")
            time.sleep(2)
            attempt += 1

        # Después del 5to intento fallido, verificar si el sistema pide recuperación de contraseña y muestra CAPTCHA
        email_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_email")))
        email_field.clear()
        email_field.send_keys("invalid_email@example.com")

        # Esperar que aparezca la opción de recuperación de clave
        recover_password_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "auth-fpp-link-bottom")))
        recover_password_button.click()

        # Verificar que se muestra la página de recuperación de contraseña con un campo de correo
        recovery_email_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_email")))
        assert recovery_email_field.is_displayed(), "El campo de correo electrónico para recuperar la contraseña no se muestra."
        print("Recuperación de contraseña activada correctamente después de 5 intentos fallidos.")

        # Verificar que se activa CAPTCHA (usamos un xpath genérico que podría cambiar según la implementación de Amazon)
        captcha = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "auth-captcha-image")))
        assert captcha.is_displayed(), "El CAPTCHA no se muestra después de 5 intentos fallidos."

    finally:
        driver.quit()

# Llamar a la prueba
test_failed_login_attempts()
