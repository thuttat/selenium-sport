from selenium.webdriver.common.by import By

from tests.pages.BasePage import BasePage


class BookingDetailPage(BasePage):
    section = "cancel"

    CANCEL_BTN = (By.CSS_SELECTOR, ".card-base button.btn-danger")
    BACK_BTN = (By.CSS_SELECTOR, "button.btn-outline")
    STATUS_BADGE = (By.CSS_SELECTOR, ".badge, [class*='badge']")
    COURT_NAME = (By.CSS_SELECTOR, "h2, .field-name")



    def cancel_booking(self):
        self.click(*self.CANCEL_BTN)

    def go_back(self):
        self.click(*self.BACK_BTN)

    def get_status(self):
        return self.find(*self.STATUS_BADGE).text

    def is_cancel_button_visible(self):
        try:
            self.wait_visible(*self.CANCEL_BTN, timeout=3)
            return True
        except Exception:
            return False
