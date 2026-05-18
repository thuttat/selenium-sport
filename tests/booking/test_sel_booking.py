import pytest
from tests.pages.LoginPage import LoginPage
from tests.pages.HomePage import HomePage
from tests.pages.CourtPage import CourtPage
from tests.pages.BookingHistoryPage import BookingHistoryPage


def login_as_user(driver, username="b", password="anhthu123@"):
    login = LoginPage(driver)
    login.login(username, password)
    login.wait_login_success()

    return driver



# TC_BOOK_01
def test_book_court_success(driver):
    login_as_user(driver)

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()

    court = CourtPage(driver)
    court.wait_url_contains("/court/")

    selected = court.select_first_available_slot()
    court.screenshot("TC_BOOK_01_slot_selected")

    if not selected:
        pytest.skip("Không có slot trống để test")

    court.confirm_booking()
    court.screenshot("TC_BOOK_01_booking_confirmed")

    court.wait_url_contains("/bookings")
    assert "/bookings" in driver.current_url


# TC_BOOK_02
def test_book_without_login(driver):
    home = HomePage(driver)
    home.open_page()
    home.click_book_first()
    home.screenshot("TC_BOOK_02_book_unauthenticated", section="booking")

    home.click_login_btn()
    home.wait_url_contains("/login")
    assert "/login" in driver.current_url


# TC_BOOK_14
def test_court_status_shows_available_or_full(driver):
    login_as_user(driver)

    home = HomePage(driver)
    home.open_page()
    home.screenshot("TC_BOOK_14_court_status_display", section="booking")
    from selenium.webdriver.common.by import By
    badges = driver.find_elements(By.CSS_SELECTOR, ".badge")
    assert len(badges) > 0, "Không có badge trạng thái nào trên trang chủ"

    badge_texts = [b.text for b in badges]
    valid = any(t in ["Available", "Full"] for t in badge_texts)
    assert valid, f"Badge không đúng: {badge_texts}"


# TC_BOOK_15
def test_booking_history_shows_bookings(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()
    history.screenshot("TC_BOOK_15_booking_history")

    assert "/bookings" in driver.current_url


# TC_BOOK_03
def test_cannot_select_past_date(driver):
    login_as_user(driver)

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()

    court = CourtPage(driver)
    court.wait_url_contains("/court/")

    date_input = court.find(*CourtPage.DATE_INPUT)
    min_date = date_input.get_attribute("min")
    court.screenshot("TC_BOOK_03_date_input_min")

    assert min_date, "Date input không có thuộc tính min"
    from datetime import date
    today = date.today().isoformat()
    assert min_date >= today
