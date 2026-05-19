from tests.pages.BasePage import BasePage, BASE_URL


class AdminPage(BasePage):
    section = "admin"
    BASE_ADMIN_URL = f"{BASE_URL}/admin"

    def _scroll_and_js_click(self, by, value):
        el = self.scroll_to_element(by, value)
        self.driver.execute_script("arguments[0].click();", el)

