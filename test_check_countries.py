import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    driver.find_element_by_xpath("//td[@id='sidebar']/descendant::span[contains(text(),'Countries')]").click()
    countries = driver.find_elements_by_xpath("//tr[@class='row']/descendant::a[not(contains(@title,'Edit'))]")
    countries_name_list = list(map(lambda x: x.text, countries))
    assert countries_name_list == sorted(countries_name_list)
    print("Countries sorted alphabetically")
    countries_link_list = list(map(lambda x: x.get_property('href'), countries))
    for i in countries_link_list:
        country = driver.find_element_by_xpath("//a[@href='%s']/following::td[1]" % i)
        zones = int(country.text)
        if zones > 0:
            edit = driver.find_element_by_xpath("//a[@href='%s']/following::td[2]" % i)
            edit.click()
            zones_in_country = list(map(lambda x: x.text, driver.find_elements_by_xpath("//table[@id='table-zones']/descendant::tr[*]/descendant::td[3]")))
            del zones_in_country[-1]
            assert zones_in_country == sorted(zones_in_country)
            print("Zones sorted alphabetically")
            driver.back()
