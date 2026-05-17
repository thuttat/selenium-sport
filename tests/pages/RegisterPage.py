from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage, BASE_URL


class RegisterPage(BasePage):
    section = "auth"
    URL = f"{BASE_URL}/register"


    FULLNAME_INPUT  = (By.CSS_SELECTOR, "input[placeholder='Enter your full name']")
    USERNAME_INPUT  = (By.CSS_SELECTOR, "input[placeholder='Enter your username']")
    EMAIL_INPUT     = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[placeholder='Enter your password (min 8 chars, 1 special)']")
    CONFIRM_INPUT   = (By.CSS_SELECTOR, "input[placeholder='Confirm your password']")
    AVATAR_INPUT    = (By.CSS_SELECTOR, "input[type='file']")
    SUBMIT_BTN      = (By.CSS_SELECTOR, "button[type='submit']")
    MSG             = (By.CSS_SELECTOR, ".error")
    LOGIN_LINK      = (By.CSS_SELECTOR, "a.link-primary")

    def open_page(self):
        self.open(self.URL)

    def fill_form(self, fullname, username, email, password, confirm):
        self.typing(*self.FULLNAME_INPUT, fullname)
        self.typing(*self.USERNAME_INPUT, username)
        self.typing(*self.EMAIL_INPUT, email)
        self.typing(*self.PASSWORD_INPUT, password)
        self.typing(*self.CONFIRM_INPUT, confirm)

    def upload_avatar(self, file_path):
        el = self.find(*self.AVATAR_INPUT)
        el.send_keys(file_path)

    def submit(self):
        self.click(*self.SUBMIT_BTN)

    def get_message(self):
        return self.wait_visible(*self.MSG).text

    def register(self, fullname, username, email, password, confirm, avatar_path=None):
        self.open_page()
        self.fill_form(fullname, username, email, password, confirm)
        if avatar_path:
            self.upload_avatar(avatar_path)
        self.submit()
