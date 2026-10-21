from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Страница «Обратная связь» (/contact)."""

    path = "/contact"

    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    TOPIC = (By.ID, "topic")
    MESSAGE = (By.ID, "message")
    CONSENT = (By.ID, "consent")
    SUBMIT = (By.ID, "submit")
    SUCCESS = (By.ID, "success")

    def fill(self, name="", email="", phone="", topic="Вопрос", message="", consent=False):
        self.type(self.NAME, name)
        self.type(self.EMAIL, email)
        self.type(self.PHONE, phone)
        Select(self.find(self.TOPIC)).select_by_visible_text(topic)
        self.type(self.MESSAGE, message)
        if self.find(self.CONSENT).is_selected() != consent:
            self.click(self.CONSENT)
        return self

    def submit(self):
        button = self.find(self.SUBMIT)
        button.click()
        self.wait.until(EC.staleness_of(button))  # форма отправляется на сервер, страница перезагружается
        return self

    def success_text(self):
        return self.text(self.SUCCESS)

    def has_success(self):
        return self.is_present(self.SUCCESS)

    def error_text(self, field):
        return self.text((By.ID, f"{field}-error"))
