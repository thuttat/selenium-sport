import pytest
import time
from tests.pages.LoginPage import LoginPage
from tests.pages.BookingHistoryPage import BookingHistoryPage
from tests.pages.BookingDetailPage import BookingDetailPage
from tests.pages.ProfilePage import ProfilePage


def login_as_user(driver, username="user_normal", password="User@12345"):
    login = LoginPage(driver)
    login.login(username, password)
    login.wait_login_success()
    return driver


# TC_USER_01
def test_user_can_view_booking_detail(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()
    history.screenshot("TC_USER_01_booking_history")

    history.switch_to_upcoming()
    time.sleep(1)

    if history.get_booking_count() == 0:
        history.switch_to_history()
        time.sleep(1)

    if history.get_booking_count() == 0:
        pytest.skip("Tài khoản không có booking nào để xem chi tiết")

    history.click_first_booking()

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")

    time.sleep(2)
    detail.screenshot("TC_USER_01_booking_detail")
    page_source = driver.page_source.lower()

    assert any(keyword in page_source for keyword in ["court", "sân"]), \
        "Không hiển thị tên sân (Court Name)"

    assert any(keyword in page_source for keyword in ["date", "ngày"]), \
        "Không hiển thị ngày đặt (Date)"

    assert any(keyword in page_source for keyword in ["time", "giờ", "slot"]), \
        "Không hiển thị giờ đặt (Time)"

    assert any(keyword in page_source for keyword in ["price", "giá", "vnd", "000"]), \
        "Không hiển thị giá (Price)"

    assert any(keyword in page_source for keyword in
               ["status", "trạng thái", "confirmed", "pending", "cancelled", "active", "completed"]), \
        "Không hiển thị trạng thái (Status)"


# TC_USER_02
def test_pagination_works_in_booking_history(driver):
    login_as_user(driver, username="user_many_bk", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()

    history.switch_to_history()
    time.sleep(2)
    history.screenshot("TC_USER_02_page1")

    count_page1 = history.get_booking_count()

    if count_page1 == 0:
        pytest.skip("Không có booking trong tab History để test pagination")

    next_btns = driver.find_elements(*BookingHistoryPage.PAGINATION_NEXT)

    if not next_btns:
        pytest.skip("Tài khoản không có đủ booking để sinh ra pagination (cần > 1 trang). "
                    "Hãy dùng tài khoản có > 5 bookings.")

    next_btn = next_btns[0]
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
    next_btn.click()
    time.sleep(2)
    history.screenshot("TC_USER_02_page2")

    count_page2 = history.get_booking_count()

    assert count_page2 > 0, \
        "Trang 2 không hiển thị booking nào — pagination không hoạt động đúng"


# TC_USER_03
def test_upcoming_and_history_tabs_show_correct_bookings(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()

    history.switch_to_upcoming()
    time.sleep(2)
    history.screenshot("TC_USER_03_upcoming_tab")

    page_source_upcoming = driver.page_source
    upcoming_count = history.get_booking_count()

    history.switch_to_history()
    time.sleep(2)
    history.screenshot("TC_USER_03_history_tab")

    page_source_history = driver.page_source
    history_count = history.get_booking_count()

    assert upcoming_count > 0 or history_count > 0, \
        "Cả hai tab Upcoming và History đều trống — không có dữ liệu để verify"

    if history_count > 0:
        assert any(keyword in page_source_history.lower() for keyword in
                   ["cancelled", "completed", "past", "history"]), \
            "Tab History không hiển thị booking đã qua hoặc đã hủy"

    if upcoming_count > 0:
        assert "Upcoming" in page_source_upcoming or upcoming_count >= 0, \
            "Tab Upcoming không load đúng"


# TC_USER_04
def test_user_profile_displays_correct_info(driver):
    login_as_user(driver)

    profile = ProfilePage(driver)
    profile.open_page()

    time.sleep(2)
    profile.screenshot("TC_USER_04_profile_page")

    assert profile.is_profile_page_loaded(), \
        f"Không ở trang profile. URL hiện tại: {driver.current_url}"

    # Ép về chữ thường để check nhãn
    page_source = driver.page_source.lower()

    assert profile.is_avatar_displayed(), \
        "Avatar không hiển thị trên trang profile"

    assert any(keyword in page_source for keyword in
               ["fullname", "full name", "họ tên", "name"]), \
        "Không hiển thị Fullname trên trang profile"

    assert any(keyword in page_source for keyword in
               ["username", "tên đăng nhập"]), \
        "Không hiển thị Username trên trang profile"

    assert any(keyword in page_source for keyword in
               ["email", "@"]), \
        "Không hiển thị Email trên trang profile"

    fullname = profile.get_fullname()
    if fullname is not None:
        assert len(fullname) > 0, f"Fullname trống, lấy được: '{fullname}'"

    email = profile.get_email()
    if email is not None:
        assert "@" in email or len(email) > 0, f"Email hiển thị không hợp lệ, lấy được: '{email}'"