from test_basic_operations import test_basic_operations
from user_data import get_and_save_user_data
from test_rate_plan import test_rate_plan
from selenium import webdriver

def run_test_rate_plan():
    # Запрашиваем и сохраняем учетные данные
    get_and_save_user_data()

    # Инициализация WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Вызов функции теста
    try:
        test_rate_plan(driver)
        test_basic_operations(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test_rate_plan()
