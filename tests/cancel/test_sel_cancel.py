import pytest
from selenium.webdriver.common.by import By

from tests.pages.CourtPage import CourtPage
from tests.pages.HomePage import HomePage
from tests.pages.LoginPage import LoginPage
from tests.pages.BookingDetailPage import BookingDetailPage
from tests.pages.BookingHistoryPage import BookingHistoryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.BasePage import BASE_URL
from datetime import date, timedelta
import time


def login_as_user(driver, username="user_normal", password="User@12345"):
    login = LoginPage(driver)
    login.login(username, password)
    login.wait_login_success()
    return driver
def go_to_first_upcoming_booking(driver):
    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    if history.get_booking_count() == 0:
        return None
    history.click_first_booking()
    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    return detail
def go_to_first_history_booking(driver):
    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_history()
    if history.get_booking_count() == 0:
        return None
    history.click_first_booking()
    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    return detail
def do_cancel_with_confirm(driver, detail):
    detail.cancel_booking()
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

# TC_CAN_01
def test_cancel_at_exact_2h_boundary(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    history.wait_visible(*BookingHistoryPage.BOOKING_CARDS)
    history.screenshot("TC_CAN_01_before_cancel", section="cancel")

    try:
        history.click_booking_by_text("Ca Boundary Đúng 2h")
    except Exception:
        pytest.skip("Không tìm thấy booking 'Ca Boundary Đúng 2h'. Hãy chạy lại seed data.")

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)
    detail.screenshot("TC_CAN_01_detail", section="cancel")

    if not detail.is_cancel_button_visible():
        pytest.skip("Không thấy nút Cancel — booking không đủ điều kiện hủy")

    detail.cancel_booking()
    detail.accept_alert()
    alert_text = detail.accept_alert()
    detail.screenshot("TC_CAN_01_after_cancel", section="cancel")

    assert "success" in alert_text.lower() or "thành công" in alert_text.lower(), \
        f"Hủy đúng 2h trước nhưng hệ thống từ chối: '{alert_text}'"


# TC_CAN_02
def test_cancel_above_2h_boundary(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    history.wait_visible(*BookingHistoryPage.BOOKING_CARDS)

    history.go_to_last_page()
    history.screenshot("TC_CAN_02_before_cancel", section="cancel")

    try:
        history.click_booking_by_text("Ca Tối Muộn")
    except Exception:
        pytest.skip("Không tìm thấy booking 'Ca tối'. Hãy chạy lại seed data.")

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)
    detail.screenshot("TC_CAN_02_detail", section="cancel")

    if not detail.is_cancel_button_visible():
        pytest.skip("Không thấy nút Cancel")

    detail.cancel_booking()
    detail.accept_alert()
    alert_text = detail.accept_alert()
    detail.screenshot("TC_CAN_02_after_cancel", section="cancel")

    assert "success" in alert_text.lower() or "thành công" in alert_text.lower(), \
        f"Hủy khi còn hơn 2h nhưng hệ thống từ chối: '{alert_text}'"


# TC_CAN_03
def test_cancel_below_2h_boundary(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    history.wait_visible(*BookingHistoryPage.BOOKING_CARDS)
    history.screenshot("TC_CAN_03_before_cancel", section="cancel")

    try:
        history.click_booking_by_text("Ca Sắp Diễn Ra < 2h")
    except Exception:
        pytest.skip("Không tìm thấy booking 'Ca Sắp Diễn Ra < 2h'. Hãy chạy lại seed data.")

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)
    detail.screenshot("TC_CAN_03_detail", section="cancel")

    if not detail.is_cancel_button_visible():
        detail.screenshot("TC_CAN_03_no_cancel_btn", section="cancel")
        return

    detail.cancel_booking()
    try:
        detail.accept_alert()
    except Exception:
        pass

    try:
        alert_text = detail.accept_alert()
        detail.screenshot("TC_CAN_03_after_attempt", section="cancel")
        assert "cannot cancel" in alert_text.lower() or "less than 2" in alert_text.lower(), \
            f"BE không từ chối hủy dưới 2h: '{alert_text}'"
    except Exception:
        detail.screenshot("TC_CAN_03_after_attempt", section="cancel")
        pytest.fail("Hủy dưới 2h nhưng không có thông báo lỗi từ hệ thống")


# TC_CAN_04
def test_unauthorized_user_cannot_cancel_others_booking(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    target_url = f"{BASE_URL}/booking/1"
    driver.get(target_url)

    detail = BookingDetailPage(driver)

    time.sleep(2)

    detail.screenshot("TC_CAN_04_IDOR_attempt", section="cancel")

    assert not detail.is_cancel_button_visible(), \
        "Lỗi bảo mật nghiêm trọng (IDOR): Nút Hủy sân xuất hiện ở đơn đặt sân của người khác!"

    detail.screenshot("TC_CAN_04_IDOR_blocked_success", section="cancel")



# TC_CAN_07
def test_cancelled_booking_moves_to_history_tab(driver):
    login_as_user(driver)

    history = BookingHistoryPage(driver)
    history.open_page()

    history.switch_to_upcoming()
    count_upcoming_before = history.get_booking_count()
    history.screenshot("TC_CAN_07_upcoming_before_cancel", section="cancel")

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
    history.screenshot("TC_CAN_07_history_after_cancel", section="cancel")

    assert count_history_after > 0, \
        "Tab History không có booking sau khi hủy — booking chưa chuyển sang History" \

# TC_CAN_05:
def test_cannot_cancel_active_booking(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    time.sleep(2)
    history.screenshot("TC_CAN_05_upcoming_list", section="cancel")

    try:
        history.click_booking_by_text('Ca Đang Diễn Ra')
    except Exception:
        pytest.fail("Không tìm thấy booking 'Ca Đang Diễn Ra'. Hãy kiểm tra lại file dummy data.")

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)
    time.sleep(1)
    detail.screenshot("TC_CAN_05_active_detail_no_cancel", section="cancel")

    assert not detail.is_cancel_button_visible(), \
        "BUGGGGGG: Sân đang trong giờ đá (Active) nhưng hệ thống vẫn hiển thị nút Hủy Sân!"

# TC_CAN_06
def test_account_restricted_after_3_cancels(driver):
    login_as_user(driver, username="user_2cancels", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    history.screenshot("TC_CAN_06_upcoming_list", section="cancel")

    try:
        history.click_booking_by_text("Sân Bóng VIP 1")
    except Exception:
        pytest.skip("Không tìm thấy booking của user_2cancels. Hãy chạy lại file dummy data.")
    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)
    time.sleep(1)
    detail.screenshot("TC_CAN_06_booking_detail", section="cancel")
    if not detail.is_cancel_button_visible():
        current_status = detail.get_status()
        pytest.fail(f"Lỗi Data: Không có nút Cancel. Trạng thái đơn hiện tại là '{current_status}'.")
    detail.cancel_booking()
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass
    time.sleep(2)
    alert_text = ""
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text.lower()
        print(f"{alert.text}")
        alert.accept()
    except Exception:
        pass
    time.sleep(1)
    detail.screenshot("TC_CAN_06_after_attempt", section="cancel")
    page_source = driver.page_source.lower()

    is_restricted_msg_shown = (
            "restricted" in page_source or "restricted" in alert_text or
            "excessive" in page_source or "excessive" in alert_text or
            "giới hạn" in page_source or "giới hạn" in alert_text or
            "khóa" in page_source or "khóa" in alert_text
    )

    assert is_restricted_msg_shown, \
        f"BUG: User đã hủy lần thứ 3 nhưng hệ thống KHÔNG hiện thông báo phạt khóa tài khoản! '{alert_text}')"

# TC_CAN_08
def test_third_cancel_still_allowed(driver):
    login_as_user(driver, username="user_2cancels", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    try:
        history.click_booking_by_text("Sân Bóng VIP 1")
    except Exception:
        pytest.skip("Không tìm thấy booking của user_2cancels để test TC_CAN_08.")

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)
    time.sleep(1)

    detail.screenshot("TC_CAN_08_before_cancel", section="cancel")

    if not detail.is_cancel_button_visible():
        pytest.fail("Lỗi Data: Không có nút Cancel để thực hiện hủy lần 3.")

    detail.cancel_booking()
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    time.sleep(2)
    alert_text = ""
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text.lower()
        alert.accept()
    except Exception:
        pass
    time.sleep(1)
    detail.screenshot("TC_CAN_08_after_cancel", section="cancel")
    page_source = driver.page_source.lower()
    restricted = (
            "restricted" in page_source or "restricted" in alert_text or
            "excessive" in page_source or "excessive" in alert_text or
            "khóa" in page_source or "khóa" in alert_text
    )

    assert not restricted, \
        f"Sai Boundary:(Log: {alert_text})"

    assert "success" in alert_text or "thành công" in alert_text, \
        f"Lỗi: Không nhận được thông báo hủy thành công.'{alert_text}'"


# TC_CAN_09
def test_booking_blocked_during_restriction(driver):
    login_as_user(driver, username="user_restricted", password="User@12345")

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()

    home.screenshot("TC_CAN_09_before_cancel", section="cancel")
    court = CourtPage(driver)
    court.wait_url_contains("/court/")
    time.sleep(2)

    if not court.select_first_available_slot():
        pytest.skip("Không có slot trống để test")

    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()

    expected_msg = "Error: Your account is temporarily restricted from booking for 24 hours due to excessive cancellations."
    court.screenshot("TC_CAN_09_after_cancel", section="cancel")
    assert expected_msg in alert_text, f"Sai thông báo Alert! Nhận được: '{alert_text}'"

#TC_CAN_10
def test_slot_restored_after_cancellation(driver):
    login_as_user(driver, username="user_normal", password="User@12345")

    history = BookingHistoryPage(driver)
    history.open_page()
    history.switch_to_upcoming()
    history.wait_visible(*BookingHistoryPage.BOOKING_CARDS)
    history.screenshot("TC_CAN_10_before_cancel", section="cancel")

    try:
        history.click_booking_by_text("Sân Bóng Thường 2")
    except Exception:
        pytest.skip("Không tìm thấy booking 'Sân Bóng Thường 2'. Hãy chạy lại seed data.")

    detail = BookingDetailPage(driver)
    detail.wait_url_contains("/booking/")
    detail.wait_visible(*BookingDetailPage.STATUS_BADGE)

    if not detail.is_cancel_button_visible():
        pytest.skip("Booking này không thể hủy")

    detail.cancel_booking()
    detail.accept_alert()  # confirm
    detail.accept_alert()  # success
    detail.screenshot("TC_CAN_10_after_cancel", section="cancel")

    login_as_user(driver, username="user_other", password="User@12345")

    home = HomePage(driver)
    home.open_page()
    home.click_book_by_name("Sân Bóng Thường 2")

    court = CourtPage(driver)
    court.wait_url_contains("/court/")

    tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    court.select_date(tomorrow_str)
    time.sleep(1)

    court.wait_visible(*CourtPage.TIMESLOTS)
    court.screenshot("TC_CAN_10_booking_screen", section="cancel")

    court.select_first_available_slot()
    court.scroll_to_element(*court.CONFIRM_BTN)
    court.click(*court.CONFIRM_BTN)

    alert_text = court.accept_alert()
    print(f"\nAlert text: {alert_text}")
    court.screenshot("TC_CAN_10_result", section="cancel")

    assert "success" in alert_text.lower() or "thành công" in alert_text.lower(), \
        f"Lỗi: Slot chưa được giải phóng sau khi hủy! BE báo: '{alert_text}'"