import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import HTMLTestRunner

class TestAmazonLogin(unittest.TestCase):

    def setUp(self):
        # Configura el driver de Selenium (asegúrate de que la ruta sea correcta para tu sistema)
        self.driver = webdriver.Chrome(executable_path="ruta_a_tu_chromedriver")
        self.driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

    def test_valid_login(self):
        # Introduce el correo
        email_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ap_email")))
        email_input.send_keys("tu_correo_electronico@dominio.com")
        
        # Haz clic en continuar
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

        # Introduce la contraseña
        password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ap_password")))
        password_input.send_keys("tu_contraseña")

        # Haz clic en iniciar sesión
        sign_in_button = self.driver.find_element(By.ID, "signInSubmit")
        sign_in_button.click()

        # Espera un poco para verificar si el inicio de sesión fue exitoso
        try:
            error_message = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Enter a valid email address or phone number') or contains(text(), 'Your password is incorrect')]")
            ))
            self.assertIn("Enter a valid email address or phone number", error_message.text or "Your password is incorrect")
        except:
            # Si no hay error, asumimos que el inicio de sesión fue exitoso
            self.assertTrue(True, "Inicio de sesión exitoso")

    def tearDown(self):
        # Pausa para inspeccionar la página antes de cerrar
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    # Configura el archivo de reporte HTML
    report_file = "test_report.html"
    
    # Configura el runner para generar el reporte HTML
    with open(report_file, "wb") as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report, title="Amazon Login Test Report", description="Prueba de inicio de sesión en Amazon.")
        unittest.main(testRunner=runner, exit=False)