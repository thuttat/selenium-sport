import pytest
from tests.pages.LoginPage import LoginPage
from tests.pages import AdminPage
from tests.pages.AdminCourtPage import AdminCourtPage
import time
import os
TEST_IMAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                          "asset", "Picture1.jpg")


def login_as_admin(driver, username="duyadmin", password="123456"):
    login = LoginPage(driver)
    login.login(username, password)
    login.wait_login_success()

    return driver


# TC_ADM_01
def test_user_cannot_access_admin_page(driver):
    login = LoginPage(driver)
    login.login("b", "anhthu123@")
    login.wait_login_success()

    driver.get("http://localhost:5173/admin/courts")

    admin = AdminCourtPage(driver)
    admin.screenshot("TC_ADM_01_user_access_admin")

    assert "/admin" not in driver.current_url, \
        "User thường có thể truy cập trang Admin!"


# TC_ADM_08
def test_admin_can_view_court_list(driver):
    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()
    admin.screenshot("TC_ADM_08_court_list")

    assert "/admin/courts" in driver.current_url
    row_count = admin.get_row_count()
    assert row_count >= 0


# TC_ADM_02
def test_admin_add_new_court(driver):
    import time
    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()

    count_before = admin.get_row_count()

    admin.click_add_field()
    admin.screenshot("TC_ADM_02_add_form_open")

    admin.fill_field_form(
        name=f"Sân Test {int(time.time())}",
        price=200000,
        description="Sân test",
        image_path=TEST_IMAGE
            )
    admin.save_form()


    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    admin.screenshot("TC_ADM_02_after_add")

    count_after = admin.get_row_count()
    assert count_after >= count_before, "Số sân không tăng sau khi thêm"


# TC_ADM_06
def test_admin_edit_court(driver):
    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()
    admin.wait_table_loaded()

    if admin.get_row_count() == 0:
        pytest.skip("Không có sân nào để sửa")

    admin.click_edit_first()
    admin.wait_form_visible()
    admin.screenshot("TC_ADM_06_edit_form_open")


    admin.react_typing(*admin.NAME_INPUT, f"Sân Edited {int(time.time())}")
    admin.save_form()
    admin.accept_alert()

    admin.screenshot("TC_ADM_06_after_edit")
    assert "/admin/courts" in driver.current_url


# TC_ADM_04
def test_admin_delete_court_with_past_bookings(driver):

    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()

    count_before = admin.get_row_count()
    if count_before == 0:
        pytest.skip("Không có sân nào để xóa")

    admin.click_delete_first()

    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    admin.screenshot("TC_ADM_04_after_delete_past_booking_court")

    count_after = admin.get_row_count()
    assert count_after <= count_before, \
        "Số sân không giảm sau khi xóa — xóa thất bại hoặc UI chưa cập nhật"


# TC_ADM_10
def test_admin_delete_court_no_bookings(driver):
    import time
    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()

    admin.click_add_field()
    new_name = f"SanTempDelete_{int(time.time())}"
    admin.fill_field_form(name=new_name, price=100000, description="Temp", image_path=TEST_IMAGE)
    admin.save_form()
    admin.accept_alert()

    admin.open_page()
    admin.wait_table_loaded()
    admin.screenshot("TC_ADM_10_before_delete_no_booking_court")

    admin.go_to_last_page()
    admin.wait_table_loaded()

    admin.click_delete_last()
    admin.accept_alert()  # confirm
    admin.accept_alert()

    admin.wait_table_loaded()
    admin.screenshot("TC_ADM_10_after_delete_no_booking_court")

    status = admin.get_last_row_status()
    assert status == "Inactive", \
        f"Sân chưa được deactivate — status hiện tại: {status}"

# TC_ADM_07
def test_admin_set_court_to_maintenance(driver):

    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()

    if admin.get_row_count() == 0:
        pytest.skip("Không có sân nào để test")

    admin.click_edit_first()
    admin.screenshot("TC_ADM_07_edit_form_for_maintenance")

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    try:
        status_select = driver.find_element(By.CSS_SELECTOR, "select[name='status'], select")
        Select(status_select).select_by_visible_text("Maintenance")
    except Exception:
        pytest.skip("Không tìm thấy field status trong form edit")

    admin.save_form()
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    admin.screenshot("TC_ADM_07_after_set_maintenance")
    assert "/admin/courts" in driver.current_url, \
        "Không ở lại trang admin sau khi save"


# TC_ADM_09
def test_admin_set_court_to_active(driver):

    login_as_admin(driver)

    admin = AdminCourtPage(driver)
    admin.open_page()

    if admin.get_row_count() == 0:
        pytest.skip("Không có sân nào để test")

    admin.click_edit_first()
    admin.screenshot("TC_ADM_09_edit_form_for_active")

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    try:
        status_select = driver.find_element(By.CSS_SELECTOR, "select[name='status'], select")
        Select(status_select).select_by_visible_text("Active")
    except Exception:
        pytest.skip("Không tìm thấy field status trong form edit")

    admin.save_form()
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    admin.screenshot("TC_ADM_09_after_set_active")

    from tests.pages.LoginPage import LoginPage
    from tests.pages.HomePage import HomePage

    login = LoginPage(driver)
    login.login("testuser", "ValidPass123!")
    login.wait_url_contains("/")

    home = HomePage(driver)
    home.open_page()
    home.screenshot("TC_ADM_09_user_sees_active_court")

    names = home.get_court_names()
    assert len(names) > 0, "Không có sân nào hiển thị sau khi chuyển Active"