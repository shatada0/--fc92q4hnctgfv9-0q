from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Общие действия для всех страниц стенда."""

    path = "/"

    def __init__(self, driver, base_url, timeout=5):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.base_url + self.path)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def is_present(self, locator):
        return bool(self.driver.find_elements(*locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text(self, locator):
        return self.find(locator).text
