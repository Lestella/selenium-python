import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_check_countries(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sidebar")))
    driver.find_element_by_xpath("//td[@id='sidebar']/descendant::span[contains(text(),'Geo Zones')]").click()
    countries = driver.find_elements_by_xpath("//tr[@class='row']/descendant::a[not(contains(@title,'Edit'))]")
    countries_link_list = list(map(lambda x: x.get_property('href'), countries))
    for i in countries_link_list:
        print(i)
        driver.find_element_by_xpath("//a[@href='%s']/following::td[2]" % i).click()
        zone = list(map(lambda x: x.text, driver.find_elements_by_xpath("//select[contains(@name,'zone_code')]/descendant::option[@selected='selected']")))
        assert zone == sorted(zone)
        driver.back()