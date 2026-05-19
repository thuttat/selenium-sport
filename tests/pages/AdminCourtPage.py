from selenium.webdriver.common.by import By
from tests.pages.AdminPage import AdminPage, BASE_URL


class AdminCourtPage(AdminPage):
    section = "admin"
    URL = f"{BASE_URL}/admin/courts"

    ADD_FIELD_BTN= (By.XPATH, "//button[contains(.,'Add Field')]")
    FORM_CARD= (By.CSS_SELECTOR, ".field-form-card")
    NAME_INPUT = (By.CSS_SELECTOR, ".field-form-card form > div:nth-child(1) > input")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[type='number']")
    DESC_INPUT = (By.CSS_SELECTOR, "textarea")
    IMAGE_INPUT= (By.CSS_SELECTOR, "input[type='file']")
    SAVE_BTN= (By.CSS_SELECTOR, ".form-actions button.btn-primary")

    TAB_ALL = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'All')]")
    TAB_FOOTBALL = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Football')]")
    TAB_BADMINTON = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Badminton')]")
    TAB_TENNIS = (By.XPATH, "//button[contains(@class,'tab-btn') and contains(.,'Tennis')]")

    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    EDIT_BTNS = (By.CSS_SELECTOR, "table tbody tr td:last-child .table-actions button:first-child")
    DELETE_BTNS= (By.CSS_SELECTOR, "table tbody tr td:last-child .table-actions button:last-child")
    LAST_ROW_BADGE = (By.CSS_SELECTOR, "table tbody tr:last-child .badge")

    PAGINATION_NEXT = (By.XPATH, "//button[contains(@class,'pagination-btn') and contains(.,'Next') and not(@disabled)]")
    PAGINATION_INFO = (By.CSS_SELECTOR, ".pagination-info")

    TOAST_MSG = (By.CSS_SELECTOR, ".toast, .alert, .notification, [role='alert'], .swal2-popup, .swal2-html-container")

    def open_page(self):
        self.open(self.URL)

    def wait_table_loaded(self):
        self.wait_visible(*self.TABLE_ROWS)

    def wait_form_visible(self):
        self.wait_visible(*self.FORM_CARD)

    def get_row_count(self):
        try:
            return len(self.finds(*self.TABLE_ROWS))
        except Exception:
            return 0

    def get_last_row_status(self):
        return self.find(*self.LAST_ROW_BADGE).text

    def find_row_by_name(self, partial_name: str):
        rows = self.finds(*self.TABLE_ROWS)
        for row in rows:
            if partial_name in row.text:
                return row
        return None

    def get_delete_btn_in_row(self, row_element):
        btns = row_element.find_elements(By.CSS_SELECTOR, ".table-actions button")
        return btns[-1] if btns else None

    def click_add_field(self):
        self._scroll_and_js_click(*self.ADD_FIELD_BTN)

    def click_edit_first(self):
        self._scroll_and_js_click(*self.EDIT_BTNS)

    def click_delete_first(self):
        self._scroll_and_js_click(*self.DELETE_BTNS)

    def click_delete_last(self):
        delete_btns = self.finds(*self.DELETE_BTNS)
        last_btn = delete_btns[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_btn)
        last_btn.click()

    def click_delete_in_row(self, row_element):
        btn = self.get_delete_btn_in_row(row_element)
        if btn is None:
            raise RuntimeError("Không tìm thấy nút Delete trong row")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

    def confirm_dialog(self):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            return True
        except Exception:
            pass

        try:
            confirm_btn = self.find_clickable(
                By.CSS_SELECTOR,
                ".swal2-confirm, button[data-testid='confirm-btn'], .modal-footer .btn-danger"
            )
            confirm_btn.click()
            return True
        except Exception:
            pass

        return False

    def get_response_message(self, timeout: int = 5) -> str:
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except Exception:
            pass

        try:
            el = self.wait_visible(*self.TOAST_MSG, timeout=timeout)
            return el.text
        except Exception:
            pass

        return ""

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

    def go_to_last_page(self):
        while True:
            try:
                self._scroll_and_js_click(*self.PAGINATION_NEXT)
                import time
                time.sleep(0.5)
            except Exception:
                break

    def go_next_page(self):
        try:
            self._scroll_and_js_click(*self.PAGINATION_NEXT)
            import time
            time.sleep(0.5)
            self.wait_table_loaded()
            return True
        except Exception:
            return False

    def filter_by_sport(self, sport: str):
        tab_map = {
            "all":       self.TAB_ALL,
            "football":  self.TAB_FOOTBALL,
            "badminton": self.TAB_BADMINTON,
            "tennis":    self.TAB_TENNIS,
        }
        self._scroll_and_js_click(*tab_map[sport.lower()])