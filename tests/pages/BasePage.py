import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TIMEOUT = 10
BASE_URL = "http://localhost:5173"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREENSHOT_BASE = os.path.join(BASE_DIR, "screenshots")
TEST_IMAGE = os.path.join(BASE_DIR, "asset", "Picture1.jpg")


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

    def accept_alert(self):
        WebDriverWait(self.driver, TIMEOUT).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def screenshot(self, filename,section =None):
        folder = os.path.join(SCREENSHOT_BASE, section or self.section)
        os.makedirs(folder, exist_ok=True)

        if not filename.endswith(".png"):
            filename = f"{filename}.png"

        path = os.path.join(folder, filename)
        self.driver.save_screenshot(path)
        print(f"\nScreenshot saved: {path}")
        return path

    def scroll_to_element(self, by, value):
        element = self.find(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def react_typing(self, by, value, text):
        el = self.find(by, value)
        el.click()
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, el, text)

    def _quote_for_xpath(self, text: str) -> str:
        if "'" in text and '"' in text:
            parts = text.split("'")
            return "concat(" + ", \"'\", ".join(f"'{p}'" for p in parts) + ")"
        if "'" in text:
            return f'"{text}"'
        return f"'{text}'"

    def find_clickable_by_text_in_card(self, text: str, card_classes=("booking-card", "card")):

        q = self._quote_for_xpath(text)
        card_cond = " or ".join([f"contains(@class, '{c}')" for c in card_classes])
        xpath = (
            f"//*[contains(normalize-space(.), {q})]/ancestor::*[{card_cond}]"
            f"//a | //*[contains(normalize-space(.), {q})]/ancestor::*[{card_cond}]//button"
        )
        return self.find_clickable(By.XPATH, xpath)
