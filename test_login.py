import pytest
from selenium import webdriver
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Safari()
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()