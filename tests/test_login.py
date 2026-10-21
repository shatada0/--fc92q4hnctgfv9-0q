from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login(driver, base_url, username, password):
    driver.get(base_url + "/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-btn").click()


def test_login_valid_credentials(driver, base_url):
    login(driver, base_url, "student", "Passw0rd!")
    logout = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "logout")))
    assert logout.text == "Logout"
    assert driver.current_url.endswith("/home")


def test_login_wrong_password(driver, base_url):
    login(driver, base_url, "student", "wrong")
    error = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "login-error")))
    assert error.text == "Неверный логин или пароль"
    assert not driver.find_elements(By.ID, "logout")
