import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os

# Crear la carpeta para los screenshots si no existe
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def take_screenshot(driver, step_name):
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"screenshots/screenshot_{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot taken: {screenshot_name}")

def test_password_recovery():
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.amazon.com/ap/forgotpassword?openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&signInRedirectToFPPThreshold=5&prepopulatedCustomerId=eyJjaXBoZXIiOiJJSlRVTDlqSFNKL1YxWnRlRWFuQ0F3PT0iLCJJViI6ImVQUkM4T0lMeERsZFpWdHM5d3JrNHc9PSIsInZlcnNpb24iOjF9&language=en_US&pageId=amzn_retail_yourorders_us&useSHuMAWorkflow=false&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fyour-orders%2Forders%3F_encoding%3DUTF8%26ref_%3Dnav_orders_first&prevRID=3C8C8NJJX4ZE24BTG2NZ&openid.assoc_handle=amzn_retail_yourorders_us&openid.mode=checkid_setup&prepopulatedLoginId=eyJjaXBoZXIiOiJGTUczY1c0WmRlSGJ0K0k1Yy9VODQ2T3NoMjJRSGxRQUpnNytDN3N6OVo4PSIsIklWIjoiNGhtR2dPYmZSRmxMc29tWmIxK3NlZz09IiwidmVyc2lvbiI6MX0%3D&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&timestamp=1732500449000")

    
    take_screenshot(driver, "page_loaded")

    
    email_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_email")))
    email_field.clear()
    email_field.send_keys("invalid_email@example.com")

    
    take_screenshot(driver, "email_entered")

    
    continue_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "continue")))
    continue_button.click()

    
    take_screenshot(driver, "continue_clicked")

    
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Enter a valid email address or phone number')]"))
    )
    assert "Enter a valid email address or phone number" in error_message.text
    print("Mensaje de error mostrado correctamente.")

    
    take_screenshot(driver, "error_message_displayed")

    
    recover_password_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "auth-fpp-link-bottom")))
    recover_password_button.click()

    
    take_screenshot(driver, "recover_password_clicked")

    
    recovery_email_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_email")))
    assert recovery_email_field.is_displayed(), "El campo de correo electrónico para recuperación de contraseña no se muestra."
    print("Página de recuperación de contraseña cargada correctamente.")

    
    take_screenshot(driver, "password_recovery_page_loaded")

    # Continuar con el flujo de recuperación de contraseña (simulado)
    email_code_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "cvf_input_email_code")))
    email_code_field.send_keys("123456")

    sms_code_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "cvf_input_sms_code")))
    sms_code_field.send_keys("654321")

    
    take_screenshot(driver, "codes_entered")

    
    new_password_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_password")))
    new_password_field.send_keys("new_secure_password")

    confirm_password_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ap_password_check")))
    confirm_password_field.send_keys("new_secure_password")

    # Tomar screenshot después de ingresar la nueva contraseña
    take_screenshot(driver, "new_password_entered")

    # Hacer clic en "Submit" para restablecer la contraseña
    submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "a-autoid-0-announce")))
    submit_button.click()

    # Verificar que la contraseña ha sido restablecida y que se puede iniciar sesión
    # Aquí se puede simular un inicio de sesión con la nueva contraseña, si es necesario.

    print("Flujo de recuperación de contraseña completado correctamente.")

    # Tomar screenshot final
    take_screenshot(driver, "test_completed")

    driver.quit()

# Llamar a la prueba
test_password_recovery()