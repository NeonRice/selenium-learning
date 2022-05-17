from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import unittest


class ascii_colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestRegistrationForm(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.required_element_cnt = 3

        self.test_links = ['http://suninjuly.github.io/registration1.html',
                           'http://suninjuly.github.io/registration2.html']

    def check_required_field_count(self):
        required_field_block = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'first_block')))
        required_fields = required_field_block.find_elements(
            By.TAG_NAME, 'input')
        return (required_fields,
                len(required_fields) == self.required_element_cnt)

    def test_required_field_count(self):
        for test_link in self.test_links:
            self.driver.get(test_link)
            found, passed = self.check_required_field_count()
            self.assertTrue(passed,
                            "Required element count changed! "
                            f"Expected: {self.required_element_cnt}, "
                            f"found: {len(found)} in link {test_link}")


def capcha_function(x):
    return math.log(math.fabs(12 * math.sin(x)))


def formatted_exception(e, message):
    print(f"{ascii_colors.RED + ascii_colors.BOLD + message}" +
          f"{ascii_colors.END + ascii_colors.YELLOW + str(e)+ ascii_colors.END}")


def submit(wait: WebDriverWait):
    # find submit button
    submit_button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[@type='submit']")))
    submit_button.click()


def solve(wait: WebDriverWait):
    input_element = wait.until(
        EC.presence_of_element_located((By.ID, "input_value")))
    if (not input_element):
        raise AssertionError("Input value not found")
    result = capcha_function(float(input_element.text))

    answer_field = driver.find_element(By.ID, "answer")
    answer_field.clear()
    answer_field.send_keys(str(result))
    answer_field.send_keys(Keys.RETURN)
    result_alert = wait.until(EC.alert_is_present())
    if not result_alert:
        raise AssertionError("Result alert no pop up")
    alert_text = result_alert.text
    result_alert.dismiss()

    if "Congrats" in alert_text:
        print(ascii_colors.GREEN + "Trial passed!\n" + ascii_colors.END +
              ascii_colors.CYAN + alert_text + ascii_colors.END)
    else:
        print(ascii_colors.RED + "Trial failed!\n" + ascii_colors.END +
              ascii_colors.YELLOW + alert_text + ascii_colors.END)
    return alert_text


if __name__ == "__main__":
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, timeout=20)
    try:
        driver.get("http://suninjuly.github.io/explicit_wait2.html")
        # submit(wait)

        book_button = driver.find_element(By.ID, "book")

        wait.until(EC.text_to_be_present_in_element((By.ID, "price"), "$100"))

        book_button.click()

        solve(wait)

        print("\nRunning unit tests...")
        unittest.main()

        assert "No results found." not in driver.page_source
    except AssertionError as e:
        formatted_exception(e, "Assertion failed! Expected:")
    except WebDriverException as e:
        formatted_exception(e, "Webdriver exception!")
    except Exception as e:
        formatted_exception(e, "Unknown exception!")
    finally:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
