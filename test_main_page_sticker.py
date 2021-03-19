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


def test_login(driver):
    driver.get("http://localhost/litecart/en/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-most-popular")))
    all_items = driver.find_elements_by_xpath("//li[@class='product column shadow hover-light']")
    print("items", len(all_items))
    for i in all_items:
        sticker = i.find_elements_by_xpath(".//div[starts-with(@class,'sticker')]")
        print("sticker", len(sticker))
        assert len(sticker) == 1
