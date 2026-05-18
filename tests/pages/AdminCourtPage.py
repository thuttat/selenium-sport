from selenium.webdriver.common.by import By
from tests.pages.AdminPage import AdminPage, BASE_URL


class AdminCourtPage(AdminPage):
    section = "admin"
    URL = f"{BASE_URL}/admin/courts"

    ADD_FIELD_BTN = (By.XPATH, "//button[contains(.,'Add Field')]")
    FORM_CARD = (By.CSS_SELECTOR, ".field-form-card")
    NAME_INPUT = (By.CSS_SELECTOR, ".field-form-card form > div:nth-child(1) > input")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[type='number']")
    DESC_INPUT  = (By.CSS_SELECTOR, "textarea")
    SAVE_BTN = (By.CSS_SELECTOR, ".form-actions button.btn-primary")

    TAB_ALL  = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'All')]")
    TAB_FOOTBALL  = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Football')]")
    TAB_BADMINTON = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Badminton')]")
    TAB_TENNIS = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Tennis')]")

    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    EDIT_BTNS  = (By.CSS_SELECTOR, "table tbody tr td:last-child .table-actions button:first-child")
    DELETE_BTNS = (By.CSS_SELECTOR, "table tbody tr td:last-child .table-actions button:last-child")
    IMAGE_INPUT = (By.CSS_SELECTOR, "input[type='file']")

    PAGINATION_NEXT = (By.XPATH,"//button[contains(@class,'pagination-btn') and contains(.,'Next') and not(@disabled)]")
    PAGINATION_INFO = (By.CSS_SELECTOR, ".pagination-info")

    LAST_ROW_BADGE = (By.CSS_SELECTOR, "table tbody tr:last-child .badge")

    def open_page(self):
        self.open(self.URL)

    def go_to_last_page(self):
        while True:
            try:
                self._scroll_and_js_click(*self.PAGINATION_NEXT)
                import time;
                time.sleep(0.5)
            except Exception:
                break

    def get_last_row_status(self):
        return self.find(*self.LAST_ROW_BADGE).text

    def click_delete_last(self):
        delete_btns = self.finds(*self.DELETE_BTNS)
        last_btn = delete_btns[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_btn)
        last_btn.click()

    def click_add_field(self):
        self._scroll_and_js_click(*self.ADD_FIELD_BTN)

    def wait_table_loaded(self):
        self.wait_visible(*self.TABLE_ROWS)

    def wait_form_visible(self):
        self.wait_visible(*self.FORM_CARD)

    def fill_field_form(self, name, price, description, field_type="football", image_path=None):
        self.wait_form_visible()
        self.react_typing(*self.NAME_INPUT, name)
        self.typing(*self.PRICE_INPUT, str(price))
        self.typing(*self.DESC_INPUT, description)
        if image_path:
            self.find(*self.IMAGE_INPUT).send_keys(image_path)

    def save_form(self):
        el = self.scroll_to_element(*self.SAVE_BTN)
        el.click()

    def get_row_count(self):
        try:
            return len(self.finds(*self.TABLE_ROWS))
        except Exception:
            return 0

    def click_edit_first(self):
        self._scroll_and_js_click(*self.EDIT_BTNS)

    def click_delete_first(self):
        self._scroll_and_js_click(*self.DELETE_BTNS)

    def filter_by_sport(self, sport):
        tab_map = {
            "all": self.TAB_ALL,
            "football": self.TAB_FOOTBALL,
            "badminton": self.TAB_BADMINTON,
            "tennis": self.TAB_TENNIS,
        }
        self._scroll_and_js_click(*tab_map[sport])