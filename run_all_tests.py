from test_rate_plan import test_rate_plan
from selenium import webdriver

def run_test_rate_plan():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        test_rate_plan(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test_rate_plan()
