from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pyautogui
from locators import LoginPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

locators = LoginPageLocators()
def login_sura(usuario, contrasenia, url_sura):

    # Inicia el navegador
    driver = webdriver.Chrome()
    driver.get(url_sura)
    driver.maximize_window()
    sleep(2)

    # Selecciona tipo de usuario
    driver.find_element(*locators.TIPO_DOCUMENTO).click()
    sleep(1)

    # Ingresa el número de documento
    driver.find_element(*locators.INPUT_USUARIO).send_keys(usuario)
    sleep(2)

    # Click en el input de la contraseña para habilitar el teclado
    driver.find_element(*locators.INPUT_CONTRASENIA).click()
    sleep(2)


    # JavaScript para encontrar el campo por XPath e insertar la contraseña
    xpath = '/html/body/div[3]/div[1]/input'  # Reemplaza con el XPath real si es diferente
    js_script = f"""
    var xpath = "{xpath}";
    var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    var input = result.singleNodeValue;
    if (input) {{
        input.removeAttribute('readonly');
        input.click();
        input.value = '{contrasenia}';
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }} else {{
        console.log('No se encontró el input con XPath');
    }}
    """

    driver.execute_script(js_script)
    sleep(2)


    # Click en el chulo verde despues de ingresar la contraseña
    aceptar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((locators.CHULO_VERDE))
    )
    aceptar_btn.click()


    # Click en el botón de inicio de sesión
    driver.find_element(*locators.CLICK_INICIAR_SESION).click()
    sleep(5)


    #Obtener cookies
    cookies = driver.get_cookies()
    for cookie in cookies:
        if 'ssoTag' in cookie['name']:
            return cookie['value']
    return None


usuario = 1053839414
contrasenia = 2025
url_sura = "https://epsapps.suramericana.com/Prestadores/"
#imagen_chulo_verde = r'C:\Users\Usuario\OneDrive\Documentos\radicacion_sura\chulo_verde.png'
#input_contraseña = pyautogui.locateOnScreen(r'C:\Users\Usuario\OneDrive\Documentos\radicacion_sura\input_contrasena.png', confidence=0.8)

cookies_login = login_sura(usuario, contrasenia, url_sura)
print(cookies_login)