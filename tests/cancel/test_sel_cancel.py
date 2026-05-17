import pytest
from tests.pages.LoginPage import LoginPage
from tests.pages.BookingDetailPage import BookingDetailPage
from tests.pages.BookingHistoryPage import BookingHistoryPage


def login_as_user(driver, username="testuser", password="ValidPass123!"):
    login = LoginPage(driver)
    login.login(username, password)
    login.wait_url_contains("/")


# TC_CAN_01
def test_cancel_booking_success(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()
    history.screenshot("TC_CAN_01_booking_list_before_cancel")

    count_before = history.get_booking_count()
    if count_before == 0:
        pytest.skip("Không có booking nào để hủy")

    history.click_first_booking()

    detail = BookingDetailPage(driver)
    detail.screenshot("TC_CAN_01_booking_detail_before_cancel")

    if not detail.is_cancel_button_visible():
        pytest.skip("Booking này không thể hủy (không còn nút Cancel)")

    detail.cancel_booking()

    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    detail.screenshot("TC_CAN_01_after_cancel")

    assert not detail.is_cancel_button_visible(), \
        "Nút Cancel vẫn còn sau khi đã hủy — trạng thái chưa cập nhật"


# TC_CAN_04
def test_cancel_button_only_visible_for_owner(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_history()
    history.screenshot("TC_CAN_04_history_tab")

    if history.get_booking_count() > 0:
        history.click_first_booking()
        detail = BookingDetailPage(driver)
        detail.screenshot("TC_CAN_04_completed_booking_detail")

        assert not detail.is_cancel_button_visible(), \
            "Booking đã hoàn thành vẫn hiển thị nút Cancel!"


# TC_CAN_07
def test_cancelled_booking_moves_to_history_tab(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()

    history.switch_to_upcoming()
    count_upcoming_before = history.get_booking_count()
    history.screenshot("TC_CAN_07_upcoming_before_cancel")

    if count_upcoming_before == 0:
        pytest.skip("Không có upcoming booking để test")

    history.click_first_booking()
    detail = BookingDetailPage(driver)
    if not detail.is_cancel_button_visible():
        pytest.skip("Booking này không thể hủy")

    detail.cancel_booking()
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    history.open_page()
    history.switch_to_history()
    count_history_after = history.get_booking_count()
    history.screenshot("TC_CAN_07_history_after_cancel")

    assert count_history_after > 0, \
        "Tab History không có booking sau khi hủy — booking chưa chuyển sang History"