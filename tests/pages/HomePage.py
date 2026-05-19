from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage, BASE_URL


class HomePage(BasePage):
    section = "home"
    URL = f"{BASE_URL}/"

    SEARCH_INPUT = (By.CSS_SELECTOR, ".filter-bar input[type='text']")
    BTN_ALL = (By.XPATH, "//div[contains(@class,'filter-buttons')]//button[text()='All']")
    BTN_FOOTBALL = (By.XPATH, "//div[contains(@class,'filter-buttons')]//button[contains(.,'Football')]")
    BTN_BADMINTON = (By.XPATH, "//div[contains(@class,'filter-buttons')]//button[contains(.,'Badminton')]")
    BTN_TENNIS = (By.XPATH, "//div[contains(@class,'filter-buttons')]//button[contains(.,'Tennis')]")
    DATE_INPUT = (By.CSS_SELECTOR, ".filter-bar input[type='date']")

    COURT_CARDS = (By.CSS_SELECTOR, ".container .court-name")
    BOOK_BTN_FIRST= (By.CSS_SELECTOR, ".grid > div:nth-child(1) .card-footer button")
    BOOK_BTN_SECOND = (By.CSS_SELECTOR, ".grid > div:nth-child(2) .card-footer button")
    EMPTY_STATE     = (By.CSS_SELECTOR, ".empty-state")

    HEADER_NAV = (By.CSS_SELECTOR, "header")
    LOGOUT_BTN = (By.XPATH, "//button[contains(.,'Logout') or contains(.,'Sign out')]")
    LOGIN_BTN = (By.XPATH, "//*[contains(text(), 'Go to the Login page')]")

    BOOK_BTN_BY_NAME_TPL = "//h3[contains(text(),'{}')]/ancestor::div[contains(@class,'card')]//button[contains(@class,'btn-primary')]"

    def click_book_by_name(self, name):
        xpath = self.BOOK_BTN_BY_NAME_TPL.format(name)
        self.click(By.XPATH, xpath)

    def open_page(self):
        self.open(self.URL)

    def search(self, keyword):
        self.typing(*self.SEARCH_INPUT, keyword)

    def filter_by_sport(self, sport):
        btn_map = {
            "all": self.BTN_ALL,
            "football": self.BTN_FOOTBALL,
            "badminton": self.BTN_BADMINTON,
            "tennis": self.BTN_TENNIS,
        }
        self.click(*btn_map[sport])

    def select_date(self, date_str):
        el = self.find(*self.DATE_INPUT)
        el.clear()
        el.send_keys(date_str)

    def get_court_names(self):
        cards = self.finds(*self.COURT_CARDS)
        return [c.text for c in cards]

    def click_book_first(self):
        self.click(*self.BOOK_BTN_FIRST)

    def click_book_second(self):
        self.click(*self.BOOK_BTN_SECOND)

    def is_empty_state_visible(self):
        try:
            self.wait_visible(*self.EMPTY_STATE, timeout=3)
            return True
        except Exception:
            return False
    def click_login_btn(self):
        self.click(*self.LOGIN_BTN)