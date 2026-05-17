from selenium.webdriver.common.by import By

from tests.pages.BasePage import BasePage, BASE_URL


class BookingHistoryPage(BasePage):
    section = "booking"
    URL = f"{BASE_URL}/bookings"

    TAB_UPCOMING    = (By.XPATH, "//button[contains(.,'Upcoming')]")
    TAB_HISTORY     = (By.XPATH, "//button[contains(.,'History') or contains(.,'Past')]")
    BOOKING_CARDS   = (By.CSS_SELECTOR, ".booking-list .booking-card, .booking-list > div")
    EMPTY_STATE     = (By.CSS_SELECTOR, ".empty-state")
    VIEW_DETAIL_BTN = (By.CSS_SELECTOR, ".booking-card a, .booking-card button")

    def open_page(self):
        self.open(self.URL)

    def switch_to_upcoming(self):
        self.click(*self.TAB_UPCOMING)

    def switch_to_history(self):
        self.click(*self.TAB_HISTORY)

    def get_booking_count(self):
        try:
            cards = self.finds(*self.BOOKING_CARDS)
            return len(cards)
        except Exception:
            return 0

    def click_first_booking(self):
        self.click(*self.VIEW_DETAIL_BTN)
