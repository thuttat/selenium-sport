from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage, BASE_URL


class LoginPage(BasePage):
    section = "auth"
    URL = f"{BASE_URL}/login"

    USERNAME_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG  = (By.CSS_SELECTOR, ".error")
    REGISTER_LINK = (By.CSS_SELECTOR, "a.link-primary")
    AVATAR_OR_NAV = (By.CSS_SELECTOR, "header .btn-primary, header img, header .user-info")

    def open_page(self):
        self.open(self.URL)

    def fill_username(self, username):
        self.typing(*self.USERNAME_INPUT, username)

    def fill_password(self, password):
        self.typing(*self.PASSWORD_INPUT, password)

    def submit(self):
        self.click(*self.SUBMIT_BTN)

    def login(self, username, password):
        self.open_page()
        self.fill_username(username)
        self.fill_password(password)
        self.submit()

    def wait_login_success(self):
        self.wait_visible(*self.AVATAR_OR_NAV)

    def get_error_message(self):
        return self.wait_visible(*self.ERROR_MSG).text

    def click_register_link(self):
        self.click(*self.REGISTER_LINK)
