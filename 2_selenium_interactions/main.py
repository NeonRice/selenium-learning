import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math


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

def capcha_function(x):
    return math.log(math.fabs(12 * math.sin(x)))

def formatted_exception(e, message):
    print(f"{ascii_colors.RED + ascii_colors.BOLD + message} {ascii_colors.END + ascii_colors.YELLOW + str(e)+ ascii_colors.END}")
    

def submit(wait: WebDriverWait):
    # find submit button
    submit_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    submit_button.click()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, timeout=10)
    try:
        driver.get("https://suninjuly.github.io/alert_accept.html")
        #assert "Cat memes" in driver.title, "Python in page title"

        submit(wait)

        # accept alert
        alert = wait.until(EC.alert_is_present())
        if (not alert):
            raise AssertionError("Alert no pop up")
        alert.accept()

        input_element = wait.until(EC.presence_of_element_located((By.ID, "input_value")))
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
        if "Congrats" in result_alert.text:
            print(ascii_colors.GREEN + "Trial passed!\n" + ascii_colors.END + ascii_colors.CYAN + result_alert.text + ascii_colors.END)
        else:
            print(ascii_colors.RED + "Trial failed!\n" + ascii_colors.END + ascii_colors.YELLOW + result_alert.text + ascii_colors.END)
            
        result_alert.dismiss()

        assert "No results found." not in driver.page_source
    except AssertionError as e:
        formatted_exception(e, "Assertion failed! Expected:")
    except WebDriverException as e:
        formatted_exception(e, "Webdriver exception!")
    except Exception as e:
        formatted_exception(e, "Unknown exception!")
    finally:
        driver.close()
    


