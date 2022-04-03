import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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


if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        driver.get("https://suninjuly.github.io/cats.html")
        driver.implicitly_wait(0.5)
        assert "Cat memes" in driver.title, "Python in page title"

        # BY CSS ELEMENT
        heading = driver.find_element(
            by=By.CSS_SELECTOR, value="h1.jumbotron-heading")
        heading.screenshot(os.path.join(os.getcwd(), "cat-memes-heading.png"))
        assert heading.text == "Cat memes", "Cat memes in page heading (jumbotron-heading css class)"

        # BY HTML TAG
        cards = driver.find_elements(by=By.CLASS_NAME, value='card')
        for card in cards:
            card_text = card.find_element(
                by=By.CLASS_NAME, value='card-text').text
            card.screenshot(os.path.join(
                os.getcwd(), card_text.replace(" ", "-")) + ".png")

        # BY XPATH
        cat_names = driver.find_elements(by=By.XPATH, value="//p[@class]")
        print(f"{ascii_colors.HEADER + ascii_colors.BOLD}Cat names{ascii_colors.END}")
        print(ascii_colors.HEADER + chr(9608) * 20 + ascii_colors.END)
        for name in cat_names:
            cat_name = name.text
            if 'cat' not in cat_name:
                continue
            print(f"{ascii_colors.CYAN + name.text + ascii_colors.END}")

        # elem.clear()
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        driver.close()
    except AssertionError as e:
        print(f"{ascii_colors.RED + ascii_colors.BOLD}Assertion failed! Expected: {ascii_colors.END + ascii_colors.YELLOW + str(e)+ ascii_colors.END}")
        driver.close()
    except WebDriverException as e:
        print(f"{ascii_colors.RED + ascii_colors.BOLD}Webdriver Exception! {ascii_colors.END + ascii_colors.YELLOW + str(e)+ ascii_colors.END}")
        driver.close()
