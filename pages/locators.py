from selenium.webdriver.common.by import By

class LoginPageLocators():
    TIPO_DOCUMENTO          = (By.XPATH, "//*[@id='ctl00_ContentMain_suraType']/option[2]")
    INPUT_USUARIO           = (By.ID, "suraName")
    INPUT_CONTRASENIA       = (By.XPATH, '//input[@name="suraPassword"]')
    CLICK_INICIAR_SESION    = (By.XPATH, "//*[@id='session-internet']")
    CHULO_VERDE             = (By.NAME, "accept")
