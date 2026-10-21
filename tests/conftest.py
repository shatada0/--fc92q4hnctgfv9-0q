import os
import threading

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from werkzeug.serving import make_server

from app import app


@pytest.fixture(scope="session")
def base_url():
    """Поднимает стенд в фоновом потоке на свободном порту."""
    server = make_server("127.0.0.1", 0, app)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


@pytest.fixture(scope="session")
def geckodriver_path():
    # Один раз на прогон: каждый install() обращается к GitHub API, а без токена там лимит 60 запросов в час
    return GeckoDriverManager().install()


@pytest.fixture
def driver(geckodriver_path):
    options = webdriver.FirefoxOptions()
    if os.getenv("FIREFOX_BIN"):  # Firefox стоит не в Program Files, geckodriver сам его не найдёт
        options.binary_location = os.environ["FIREFOX_BIN"]
    if os.getenv("CI"):
        options.add_argument("-headless")
    driver = webdriver.Firefox(service=Service(geckodriver_path), options=options)
    yield driver
    driver.quit()
