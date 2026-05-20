import pytest
from tests.pages.LoginPage import LoginPage
from tests.pages.HomePage import HomePage
from tests.pages.CourtPage import CourtPage
from tests.pages.BookingHistoryPage import BookingHistoryPage


def login_as_user(driver, username="user_normal", password="User@12345"):
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

# TC_BOOK_06
def test_cannot_book_more_than_3_per_day(driver):
    login_as_user(driver, username="user_3bookings", password="User@12345")

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()

    court = CourtPage(driver)
    court.wait_url_contains("/court/")

    if not court.select_first_available_slot():
        pytest.skip("Không có slot trống")

    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)

    alert_text = court.accept_alert()
    court.screenshot("TC_BOOK_06_quota_exceeded", section="booking")

    assert "3" in alert_text or "maximum" in alert_text.lower() or "quota" in alert_text.lower(), \
        f"Không có thông báo giới hạn booking: '{alert_text}'"


# TC_BOOK_07
def test_cannot_book_already_booked_slot(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    home = HomePage(driver)
    home.open_page()
    home.click_book_by_name("Sân Bóng VIP 1 (5 người)")

    court = CourtPage(driver)
    court.wait_url_contains("/court/")
    court.select_tomorrow()

    court.scroll_to_element(*court.TIMESLOTS)
    court.find(*court.TIMESLOTS).click()
    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)
    court.accept_alert()

    login_as_user(driver, username="user_2bookings", password="User@12345")

    home.open_page()
    home.click_book_by_name("Sân Bóng VIP 1 (5 người)")

    court.wait_url_contains("/court/")
    court.select_tomorrow()

    court.scroll_to_element(*court.TIMESLOTS)
    court.find(*court.TIMESLOTS).click()
    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)

    alert_text = court.accept_alert()
    court.screenshot("TC_BOOK_07_time_conflict", section="booking")

    assert "already booked" in alert_text.lower() or "conflict" in alert_text.lower(), \
        f"Không có thông báo conflict: '{alert_text}'"


# TC_BOOK_15
def test_booking_different_court_types(driver):
    login_as_user(driver, username="user_many_bk", password="User@12345")

    # Football
    home = HomePage(driver)
    home.open_page()
    home.click_book_by_name("Sân Bóng VIP 1 (5 người)")
    court = CourtPage(driver)
    court.wait_url_contains("/court/")
    court.select_tomorrow()
    court.scroll_to_element(*court.TIMESLOTS)
    court.find(*court.TIMESLOTS).click()
    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)
    alert_text = court.accept_alert()
    assert "success" in alert_text.lower(), f"Đặt Football thất bại: '{alert_text}'"
    court.screenshot("TC_BOOK_15_football", section="booking")

    # Tennis
    home.open_page()
    home.click_book_by_name("Sân Tennis Chuẩn ATP")
    court.wait_url_contains("/court/")
    court.select_tomorrow()
    court.scroll_to_element(*court.TIMESLOTS)
    court.find(*court.TIMESLOTS).click()
    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)
    alert_text = court.accept_alert()
    assert "success" in alert_text.lower(), f"Đặt Tennis thất bại: '{alert_text}'"
    court.screenshot("TC_BOOK_15_tennis", section="booking")

    # Badminton
    home.open_page()
    home.click_book_by_name("Sân Cầu Lông Số 1")
    court.wait_url_contains("/court/")
    court.select_tomorrow()
    court.scroll_to_element(*court.TIMESLOTS)
    court.find(*court.TIMESLOTS).click()
    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)
    alert_text = court.accept_alert()
    assert "success" in alert_text.lower(), f"Đặt Badminton thất bại: '{alert_text}'"
    court.screenshot("TC_BOOK_15_badminton", section="booking")


# TC_BOOK_16
def test_third_booking_same_day_success(driver):
    login_as_user(driver, username="user_2bookings", password="User@12345")

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()

    court = CourtPage(driver)
    court.wait_url_contains("/court/")

    if not court.select_first_available_slot():
        pytest.skip("Không có slot trống")

    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)

    alert_text = court.accept_alert()
    court.screenshot("TC_BOOK_16_third_booking", section="booking")

    assert "success" in alert_text.lower() or "thành công" in alert_text.lower(), \
        f"Booking thứ 3 trong ngày thất bại: '{alert_text}'"
