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
    VIEW_BTNS = (By.CSS_SELECTOR, ".booking-card .actions button.btn-outline")

    DYNAMIC_CARD_BTN_TPL = "//*[contains(text(), '{}')]/ancestor::*[contains(@class, 'booking-card') or contains(@class, 'card')]//*[self::a or self::button]"

    PAGINATION_NEXT = (By.XPATH,"//button[contains(@class,'pagination-btn') and contains(.,'Next') and not(@disabled)]")

    def go_to_last_page(self):
        while True:
            try:
                next_btn = self.find_clickable(*self.PAGINATION_NEXT)
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
                next_btn.click()
                import time;
                time.sleep(0.5)
            except Exception:
                break
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



    def click_booking_by_text(self, text):
        btn = self.find_clickable_by_text_in_card(text)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()

    def click_booking_by_index(self, index):
        view_btns = self.finds(*self.VIEW_BTNS)
        if not view_btns or index >= len(view_btns):
            raise Exception(f"Không tìm thấy booking ở index {index}. Hiện có {len(view_btns)} booking.")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btns[index])
        view_btns[index].click()