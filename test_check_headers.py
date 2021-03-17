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


def test_check_headers(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sidebar")))
    menu_items = list(map(lambda x: x.text, driver.find_elements_by_xpath("//td[@id='sidebar']/descendant::li[@id='app-']")))
    for i in menu_items:
        top_item = driver.find_element_by_xpath("//span[contains(text(),'%s')]" % i)
        top_item.click()
        header = driver.find_elements_by_xpath("//h1")
        assert len(header) > 0
        submenu_items = list(map(lambda x: x.text, driver.find_elements_by_xpath("//ul[@class='docs']/descendant::li[*]")))
        for j in submenu_items:
            submenu_item = driver.find_element_by_xpath("//li[starts-with(@id,'doc-')]/descendant::span[contains(text(),'%s')]" % j)
            submenu_item.click()
            header = driver.find_elements_by_xpath("//h1")
            assert len(header) > 0