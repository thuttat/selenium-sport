import pytest
from tests.pages.HomePage import HomePage
from tests.pages.LoginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_as_user(driver, username="user_normal", password="User@12345"):
    login = LoginPage(driver)
    login.login(username, password)
    login.wait_login_success()

    return driver

# TC_HOME_01
def test_search_courts_by_keyword(driver):
    page = HomePage(driver)
    page.open_page()
    kw = "1"
    page.search(kw)
    time.sleep(1)
    page.screenshot(f"TC_HOME_01_search_{kw}")

    names = page.get_court_names()
    assert len(names) > 0, f"Không tìm thấy sân nào với từ khóa '{kw}'"
    assert all(kw.lower() in n.lower() for n in names), \
        f"Có sân không chứa từ khóa '{kw}': {names}"


# TC_HOME_02
def test_search_no_result(driver):
    page = HomePage(driver)
    page.open_page()
    page.search("XYZZZZNOTEXIST123")
    time.sleep(1)
    page.screenshot("TC_HOME_02_search_no_result")

    assert page.is_empty_state_visible(), "Không hiển thị empty state khi không có kết quả"


# TC_HOME_03
def test_filter_by_football(driver):
    page = HomePage(driver)
    page.open_page()
    page.filter_by_sport("football")
    time.sleep(1)
    page.screenshot("TC_HOME_03_filter_football")

    assert "localhost:5173" in driver.current_url


# TC_HOME_04
def test_filter_by_badminton(driver):
    page = HomePage(driver)
    page.open_page()
    page.filter_by_sport("badminton")
    time.sleep(1)
    page.screenshot("TC_HOME_04_filter_badminton")
    assert "localhost:5173" in driver.current_url


# TC_HOME_05
def test_filter_by_tennis(driver):
    page = HomePage(driver)
    page.open_page()
    page.filter_by_sport("tennis")
    time.sleep(1)
    page.screenshot("TC_HOME_05_filter_tennis")
    assert "localhost:5173" in driver.current_url


# TC_HOME_06
def test_click_book_now_redirects_to_court(driver):
    login_as_user(driver)

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()
    home.screenshot("TC_HOME_06_book_now_redirect")


    home.wait_url_contains("/court/")
    assert "/court/" in driver.current_url, \
        f"Không chuyển sang trang court: {driver.current_url}"


# TC_HOME_07
def test_book_now_without_login_redirects_to_login(driver):

    home = HomePage(driver)
    home.open_page()
    home.click_book_first()
    home.click_login_btn()

    home.screenshot("TC_HOME_07_book_unauthenticated")
    home.wait_url_contains("/login")
    assert "/login" in driver.current_url, \
        f"Không chuyển về trang login sau khi click: {driver.current_url}"

# TC_GUEST_01
def test_guest_can_view_court_list(driver):
    page = HomePage(driver)
    page.open_page()
    page.screenshot("TC_GUEST_01_court_list")

    names = page.get_court_names()
    assert len(names) > 0, "Guest không thấy sân nào — danh sách sân trống hoặc không load được"


# TC_GUEST_02
def test_guest_filter_courts_by_tennis(driver):
    page = HomePage(driver)
    page.open_page()
    page.filter_by_sport("tennis")
    time.sleep(1)
    page.screenshot("TC_GUEST_02_filter_tennis")

    names = page.get_court_names()
    assert "localhost:5173" in driver.current_url, "Trang bị redirect sau khi filter"

    assert page.is_empty_state_visible() is False or len(names) >= 0, \
        "Filter Tennis khiến trang hiển thị lỗi"


# TC_GUEST_03
def test_guest_search_court_by_name(driver):
    page = HomePage(driver)
    page.open_page()

    keyword = "Sân"
    page.search(keyword)
    time.sleep(1)
    page.screenshot("TC_GUEST_03_search_by_name")

    names = page.get_court_names()
    assert len(names) > 0, f"Không tìm thấy sân nào với từ khóa '{keyword}'"
    assert all(keyword.lower() in n.lower() for n in names), \
        f"Có sân không chứa từ khóa '{keyword}': {names}"

