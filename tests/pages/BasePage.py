import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 10
BASE_URL = "http://localhost:5173"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREENSHOT_BASE = os.path.join(BASE_DIR, "screenshots")


class BasePage:
    section = "general"

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )

    def finds(self, by, value):
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def find_clickable(self, by, value):
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((by, value))
        )

    def typing(self, by, value, text):
        e = self.find(by, value)
        e.clear()
        e.send_keys(text)

    def click(self, by, value):
        e = self.find_clickable(by, value)
        e.click()


    def wait_url_contains(self, partial_url, timeout=TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url)
        )

    def wait_url_to_be(self, url, timeout=TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )

    def wait_visible(self, by, value, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_text_in_element(self, by, value, text, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((by, value), text)
        )

    def screenshot(self, filename):
        folder = os.path.join(SCREENSHOT_BASE, self.section)
        os.makedirs(folder, exist_ok=True)

        if not filename.endswith(".png"):
            filename = f"{filename}.png"

        path = os.path.join(folder, filename)
        self.driver.save_screenshot(path)
        print(f"\nScreenshot saved: {path}")
        return path
