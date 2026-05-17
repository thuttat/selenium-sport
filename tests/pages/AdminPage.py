from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage, BASE_URL


class AdminCourtPage(BasePage):
    section = "admin"
    URL = f"{BASE_URL}/admin/courts"

    ADD_FIELD_BTN   = (By.XPATH, "//button[contains(.,'Add Field')]")
    CANCEL_FORM_BTN = (By.XPATH, "//button[contains(.,'Cancel')]")

    NAME_INPUT      = (By.CSS_SELECTOR, "input[name='name'], input[placeholder*='name'], input[placeholder*='Name']")
    TYPE_SELECT     = (By.CSS_SELECTOR, "select[name='field_type'], select")
    PRICE_INPUT     = (By.CSS_SELECTOR, "input[name='price_per_hour'], input[type='number']")
    DESC_INPUT      = (By.CSS_SELECTOR, "textarea[name='description'], textarea")
    IMAGE_INPUT     = (By.CSS_SELECTOR, "input[type='file']")
    SAVE_BTN        = (By.CSS_SELECTOR, "button[type='submit']")

    TAB_ALL         = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'All')]")
    TAB_FOOTBALL    = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Football')]")
    TAB_BADMINTON   = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Badminton')]")
    TAB_TENNIS      = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Tennis')]")

    TABLE_ROWS      = (By.CSS_SELECTOR, "table tbody tr, .field-table tbody tr")
    EDIT_BTNS       = (By.XPATH, "//button[contains(.,'Edit')]")
    DELETE_BTNS     = (By.XPATH, "//button[contains(.,'Delete') or contains(.,'Deactivate')]")

    def open_page(self):
        self.open(self.URL)

    def click_add_field(self):
        self.click(*self.ADD_FIELD_BTN)

    def fill_field_form(self, name, price, description, field_type="football"):
        self.typing(*self.NAME_INPUT, name)
        self.typing(*self.PRICE_INPUT, str(price))
        self.typing(*self.DESC_INPUT, description)

    def save_form(self):
        self.click(*self.SAVE_BTN)

    def get_row_count(self):
        try:
            rows = self.finds(*self.TABLE_ROWS)
            return len(rows)
        except Exception:
            return 0

    def click_edit_first(self):
        self.click(*self.EDIT_BTNS)

    def click_delete_first(self):
        self.click(*self.DELETE_BTNS)

    def filter_by_sport(self, sport):
        tab_map = {
            "all": self.TAB_ALL,
            "football": self.TAB_FOOTBALL,
            "badminton": self.TAB_BADMINTON,
            "tennis": self.TAB_TENNIS,
        }
        self.click(*tab_map[sport])
