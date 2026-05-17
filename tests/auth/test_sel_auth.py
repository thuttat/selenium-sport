import pytest
from tests.pages.LoginPage import LoginPage
from tests.pages.RegisterPage import RegisterPage
from tests.pages.HomePage import HomePage



# TC_LOG_01
def test_login_success(driver):
    page = LoginPage(driver)
    page.login("admin", "admin123")
    page.screenshot("TC_LOG_01_login_success")

    page.wait_url_contains("/")
    assert "/login" not in driver.current_url, "Vẫn còn ở trang login sau khi đăng nhập"


# TC_LOG_02
def test_login_wrong_password(driver):
    page = LoginPage(driver)
    page.login("validuser", "WrongPass999!")
    page.screenshot("TC_LOG_02_wrong_password")

    error = page.get_error_message()
    assert error, "Không có thông báo lỗi khi sai mật khẩu"


# TC_LOG_03
def test_login_nonexistent_username(driver):
    page = LoginPage(driver)
    page.login("userkhongtontai_xyz", "AnyPass123!")
    page.screenshot("TC_LOG_03_nonexistent_username")

    error = page.get_error_message()
    assert error, "Không có thông báo lỗi khi username không tồn tại"

# TC_REG_01
def test_register_success(driver, tmp_path):
    import time
    avatar = tmp_path / "avatar.png"
    avatar.write_bytes(b"\x89PNG\r\n" + b"\x00" * 100)

    page = RegisterPage(driver)
    page.register(
        fullname="Test User Sel",
        username=f"seluser_{int(time.time())}",
        email=f"sel_{int(time.time())}@gmail.com",
        password="ValidPass123!",
        confirm="ValidPass123!",
        avatar_path=str(avatar)
    )
    page.screenshot("TC_REG_01_register_success")

    page.wait_url_contains("/login")
    assert "/login" in driver.current_url


# TC_REG_04
def test_register_passwords_not_match(driver, tmp_path):
    avatar = tmp_path / "avatar.png"
    avatar.write_bytes(b"\x89PNG\r\n" + b"\x00" * 100)

    page = RegisterPage(driver)
    page.register(
        fullname="Test User",
        username="testuser123",
        email="test@gmail.com",
        password="ValidPass123!",
        confirm="DifferentPass999!",
        avatar_path=str(avatar)
    )
    page.screenshot("TC_REG_04_password_mismatch")

    msg = page.get_message()
    assert "match" in msg.lower() or "password" in msg.lower(), \
        f"Thông báo lỗi không đúng: {msg}"


# TC_REG_07
def test_register_missing_avatar(driver):
    page = RegisterPage(driver)
    page.register(
        fullname="Test User",
        username="testuser123",
        email="test@gmail.com",
        password="ValidPass123!",
        confirm="ValidPass123!",
        avatar_path=None
    )
    page.screenshot("TC_REG_07_missing_avatar")

    msg = page.get_message()
    assert msg, "Không có thông báo lỗi khi thiếu avatar"



# TC_OUT_01
def test_logout_success(driver):
    login_page = LoginPage(driver)
    login_page.login("admin", "admin123")
    login_page.wait_url_contains("/")

    home = HomePage(driver)
    home.click(*home.LOGOUT_BTN)
    home.screenshot("TC_OUT_01_logout_success")

    home.wait_url_contains("/login")
    assert "/login" in driver.current_url


# TC_OUT_02
def test_access_protected_page_after_logout(driver):
    login_page = LoginPage(driver)
    login_page.login("admin", "admin123")
    login_page.wait_url_contains("/")

    home = HomePage(driver)
    home.click(*home.LOGOUT_BTN)
    home.wait_url_contains("/login")

    driver.get("http://localhost:5173/bookings")
    home.screenshot("TC_OUT_02_access_after_logout")

    home.wait_url_contains("/login")
    assert "/login" in driver.current_url, "Có thể truy cập trang protected sau logout!"
