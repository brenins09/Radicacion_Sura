from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def limpiar_input(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).clear()

    def get_text(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
    
    def navigate_to(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title
    
    def send_arrow_down(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        element.send_keys(Keys.DOWN)
        element.send_keys(Keys.ENTER)

    def send_esc(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).send_keys(Keys.ESCAPE)

    def send_tab(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).send_keys(Keys.TAB)

    def send_delete(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.DELETE)

    def input_file(self, locator, file_path):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator)).send_keys(file_path)

    def scroll(self, locator):
        element =  WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
