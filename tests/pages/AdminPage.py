from tests.pages.BasePage import BasePage, BASE_URL


class AdminPage(BasePage):
    section = "admin"
    BASE_ADMIN_URL = f"{BASE_URL}/admin"

    def _scroll_and_js_click(self, by, value):
        el = self.scroll_to_element(by, value)
        self.driver.execute_script("arguments[0].click();", el)

    def react_typing(self, by, value, text):
        el = self.find(by, value)
        el.click()
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, el, text)