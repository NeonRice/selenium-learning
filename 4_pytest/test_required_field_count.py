from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


class Test:
    def test_required_field_count_1(self, driver, wait, required_element_cnt):
        driver.get('http://suninjuly.github.io/registration1.html')
        found, passed = check_required_field_count(wait, required_element_cnt)
        assert passed,  ("Required element count changed! " +
                         f"Expected: {required_element_cnt}, " +
                         f"found: {len(found)}")

    def test_required_field_count_2(self, driver, wait, required_element_cnt):
        driver.get('http://suninjuly.github.io/registration2.html')
        found, passed = check_required_field_count(wait, required_element_cnt)
        assert passed,  ("Required element count changed! " +
                         f"Expected: {required_element_cnt}, " +
                         f"found: {len(found)}")


@pytest.fixture()
def required_element_cnt():
    return 3


def check_required_field_count(wait, required_element_cnt):
    required_field_block = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'first_block')))
    required_fields = required_field_block.find_elements(
        By.TAG_NAME, 'input')
    return (required_fields,
            len(required_fields) == required_element_cnt)


@pytest.fixture(autouse=True, scope='session')
def driver():
    driver = webdriver.Chrome()
    yield driver
    # Teardown

    driver.close()


@pytest.fixture(scope='function')
def wait(driver):
    return WebDriverWait(driver, timeout=10)
