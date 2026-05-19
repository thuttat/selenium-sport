from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage, BASE_URL


class ProfilePage(BasePage):
    section = "user"
    URL = f"{BASE_URL}/profile"

    FULLNAME = (By.CSS_SELECTOR, "input.profile-input-field[value]")
    USERNAME = (By.CSS_SELECTOR, "h3.profile-username")
    EMAIL = (By.CSS_SELECTOR, "input[type='email'].profile-input-field")
    AVATAR = (By.CSS_SELECTOR, ".profile-avatar-img")

    def open_page(self):
        self.open(self.URL)

    def get_fullname(self):
        try:
            return self.wait_visible(*self.FULLNAME).get_attribute("value").strip()
        except Exception:
            return ""

    def get_email(self):
        try:
            return self.wait_visible(*self.EMAIL).get_attribute("value").strip()
        except Exception:
            return ""

    def get_username(self):
        try:
            return self.wait_visible(*self.USERNAME).text.strip()
        except Exception:
            return ""


    def is_avatar_displayed(self):
        try:
            avatar = self.wait_visible(*self.AVATAR, timeout=5)
            return avatar.is_displayed()
        except Exception:
            return False

    def is_profile_page_loaded(self):
        try:
            self.wait_url_contains("/profile")
            return True
        except Exception:
            return False
