import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    base_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path_windows = os.path.join(base_dir, '.venv', 'chromedriver.exe')

    if os.path.exists(driver_path_windows):
        service = Service(executable_path=driver_path_windows)
    else:
        service = Service()

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
