"""ЛР3, п.2: открыть браузер, загрузить страницу и закрыть браузер.

Стенд должен быть запущен: .venv/Scripts/python app.py
Запуск: .venv/Scripts/python scripts/open_browser.py [url]
"""
import os
import sys

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000/login"

options = webdriver.FirefoxOptions()
if os.getenv("FIREFOX_BIN"):  # Firefox стоит не в Program Files, geckodriver сам его не найдёт
    options.binary_location = os.environ["FIREFOX_BIN"]
if os.getenv("CI"):
    options.add_argument("-headless")

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
try:
    driver.get(url)
    print("Открыта страница:", driver.current_url, "| заголовок:", driver.title)
finally:
    driver.quit()
    print("Браузер закрыт")
