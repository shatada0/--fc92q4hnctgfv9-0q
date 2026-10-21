"""ЛР7: запуск приложения «Заметки» на эмуляторе и тап по кнопке «Добавить».

Перед запуском:
  1. собрать APK:          cd mobile && gradlew assembleDebug
  2. запустить эмулятор:   emulator -avd Pixel_10a
  3. запустить Appium:     appium
Запуск: .venv/Scripts/python -m pytest mobile/test_notes.py -v
"""
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

APK = Path(__file__).parent / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
ID = "com.example.notes:id/"


@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.app = str(APK)  # Appium ставит APK и перед сессией очищает данные приложения
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()


def test_add_note(driver):
    driver.find_element(AppiumBy.ID, ID + "noteInput").send_keys("Купить хлеб")
    driver.find_element(AppiumBy.ID, ID + "addButton").click()

    notes = driver.find_elements(AppiumBy.ID, "android:id/text1")
    assert [note.text for note in notes] == ["Купить хлеб"]
    assert driver.find_element(AppiumBy.ID, ID + "counter").text == "Заметок: 1"
