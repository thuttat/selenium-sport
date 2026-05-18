from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage
from tests.pages.BookingDetailPage import BookingDetailPage


class CourtPage(BasePage):
    section = "booking"

    DATE_INPUT= (By.CSS_SELECTOR, "input[type='date']")
    TIMESLOTS = (By.XPATH, "//*[@id='root']/div/main/div/div/div[3]/div/div/button[6]")
    CONFIRM_BTN= (By.XPATH, "//button[contains(.,'Confirm') or contains(.,'Book')]")
    BACK_BTN= (By.XPATH, "//button[contains(.,'Back')]")
    COURT_NAME = (By.CSS_SELECTOR, ".booking-header h2, .court-title, h2")
    LOADING  = (By.CSS_SELECTOR, ".loading")
    SUMMARY_TOTAL = (By.CSS_SELECTOR, ".summary-card-wrapper, .booking-summary")
    SLOT_SELECTED = (By.CSS_SELECTOR, "button.btn.slot.selected")

    def select_date(self, date_str):
        el = self.find(*self.DATE_INPUT)
        el.clear()
        el.send_keys(date_str)

    def get_available_slots(self):
        slots = self.finds(*self.TIMESLOTS)
        return [s for s in slots if s.is_enabled()]

    def select_first_available_slot(self):
        slots = self.get_available_slots()
        if slots:
            self.scroll_to_element(*self.TIMESLOTS)
            slots[0].click()
            print(f"\nSlot class after click: {slots[0].get_attribute('class')}")
            self.wait_visible(*self.SLOT_SELECTED)
            return True
        return False


    def confirm_booking(self):
        self.scroll_to_element(*self.CONFIRM_BTN)
        self.click(*self.CONFIRM_BTN)
        self.accept_alert()

    def go_back(self):
        self.click(*self.BACK_BTN)

    def get_court_name(self):
        return self.find(*self.COURT_NAME).text


