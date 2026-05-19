import time
from datetime import date, timedelta
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.RegisterPage import RegisterPage
from tests.pages.LoginPage import LoginPage
from tests.pages.HomePage import HomePage
from tests.pages.CourtPage import CourtPage
from tests.pages.BookingHistoryPage import BookingHistoryPage
from tests.pages.BookingDetailPage import BookingDetailPage
from tests.pages.AdminCourtPage import AdminCourtPage
from tests.pages.BasePage import TEST_IMAGE, BASE_URL


def login(driver, username, password):
    page = LoginPage(driver)
    page.login(username, password)
    page.wait_login_success()


def logout(driver):
    driver.delete_all_cookies()
    driver.get(BASE_URL)


def _do_book_court(driver, court_name=None):
    home = HomePage(driver)

    if court_name:
        home.click_book_by_name(court_name)
    else:
        home.click_book_first()

    court = CourtPage(driver)
    court.wait_url_contains("/court/")

    tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    court.select_date(tomorrow_str)
    time.sleep(1)

    court.scroll_to_element(*court.TIMESLOTS)
    if not court.select_first_available_slot():
        return None

    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        text = driver.switch_to.alert.text
        driver.switch_to.alert.accept()
        return text
    except Exception:
        return ""


def book_first_available_court(driver, court_name=None):
    home = HomePage(driver)
    home.open_page()
    time.sleep(1)
    return _do_book_court(driver, court_name=court_name)


def admin_add_court(driver, court_name):
    admin = AdminCourtPage(driver)
    admin.open_page()
    admin.click_add_field()
    admin.wait_form_visible()

    admin.fill_field_form(
        name=court_name,
        price=150000,
        description="Sân tạo từ kịch bản E2E",
        image_path=TEST_IMAGE,
    )
    admin.save_form()

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception:
        pass

    time.sleep(1)
    return True


def cancel_first_upcoming(driver):
    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    time.sleep(1)

    if history.get_booking_count() == 0:
        return False

    history.click_first_booking()
    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")

    if not detail.is_cancel_button_visible():
        return False

    detail.cancel_booking()
    try:
        driver.switch_to.alert.accept()
        time.sleep(1)
        driver.switch_to.alert.accept()
    except Exception:
        pass

    time.sleep(1)
    return True


#TC_E2E_01
def test_TC_E2E_01_register_book_and_cancel_flow(driver):

    new_username = f"e2e_user_{int(time.time())}"
    register = RegisterPage(driver)
    register.register(
        fullname="E2E Tester",
        username=new_username,
        email=f"{new_username}@gmail.com",
        password="Password@123!",
        confirm="Password@123!",
        avatar_path=TEST_IMAGE,
    )

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception:
        pass

    register.wait_url_contains("/login", timeout=10)
    register.screenshot("TC_E2E_01_after_register", section="e2e")

    login(driver, new_username, "Password@123!")

    home = HomePage(driver)
    home.open_page()
    time.sleep(1)

    alert_text = None
    book_buttons = driver.find_elements(By.CSS_SELECTOR, ".court-card .btn, .field-card .btn, .card .btn-primary")
    for i in range(len(book_buttons)):
        home.open_page()
        time.sleep(1)
        btns = driver.find_elements(By.CSS_SELECTOR, ".court-card .btn, .field-card .btn, .card .btn-primary")
        if i >= len(btns):
            break
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btns[i])
        btns[i].click()

        court = CourtPage(driver)
        court.wait_url_contains("/court/")
        tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        court.select_date(tomorrow_str)
        time.sleep(1)

        court.scroll_to_element(*court.TIMESLOTS)
        if not court.select_first_available_slot():
            driver.back()
            time.sleep(1)
            continue

        court.scroll_to_element(*court.CONFIRM_BTN)
        court.click(*court.CONFIRM_BTN)

        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = driver.switch_to.alert.text
            driver.switch_to.alert.accept()
        except Exception:
            alert_text = ""
        break

    if alert_text is None:
        pytest.skip("Không có slot trống cho ngày mai.")

    CourtPage(driver).screenshot("TC_E2E_01_after_book", section="e2e")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    time.sleep(1)

    if history.get_booking_count() == 0:
        pytest.fail("Vừa đặt xong nhưng không thấy booking trong Upcoming tab!")

    history.click_first_booking()
    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")

    if not detail.is_cancel_button_visible():
        pytest.fail("Vào detail booking nhưng không thấy nút Cancel!")

    detail.cancel_booking()
    try:
        driver.switch_to.alert.accept()  # confirm
        time.sleep(1)
        driver.switch_to.alert.accept()  # success
    except Exception:
        pass

    detail.screenshot("TC_E2E_01_after_cancel", section="e2e")

    assert not detail.is_cancel_button_visible(), \
        "LỖI: Hủy xong nhưng nút Cancel vẫn còn hiển thị!"


#TC_E2E_02
def test_TC_E2E_02_admin_adds_court_user_books_it(driver):
    court_name = f"San Z E2E {int(time.time())}"

    login(driver, "duyadmin", "Admin@12345")
    admin_add_court(driver, court_name)
    AdminCourtPage(driver).screenshot("TC_E2E_02_after_admin_add", section="e2e")

    logout(driver)
    login(driver, "user_normal", "User@12345")

    home = HomePage(driver)
    home.open_page()
    time.sleep(1)
    home.search(court_name)
    time.sleep(2)
    home.screenshot("TC_E2E_02_search_result", section="e2e")

    alert_text = _do_book_court(driver, court_name=court_name)
    if alert_text is None:
        pytest.skip("Không có slot trống cho Court Z.")

    CourtPage(driver).screenshot("TC_E2E_02_after_book", section="e2e")

    assert "success" in alert_text.lower() or "thành công" in alert_text.lower(), \
        f"Court Z tạo xong nhưng user đặt thất bại. Alert: '{alert_text}'"


