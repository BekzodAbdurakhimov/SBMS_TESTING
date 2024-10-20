from tests.test_rate_plan import test_rate_plan
from tests.test_serv_activate import test_serv_activate
from tests.test_serv_deactivate import test_serv_deactivate
from tests.test_sms_pack_activate import test_pack_activate
from tests.test_sms_pack_deactivate import test_pack_deactivate
from tests.test_internet_pack_activate import test_internet_pack_activate
from tests.test_internet_pack_deactivate import test_internet_pack_deactivate
from selenium import webdriver

def run_test_rate_plan():
    # Запрашиваем и сохраняем учетные данные
    # get_and_save_user_data()

    # Инициализация WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Вызов функции теста
    try:
        test_rate_plan(driver)
        test_serv_activate(driver)
        test_serv_deactivate(driver)
        test_pack_activate(driver)
        test_pack_deactivate(driver)
        test_internet_pack_activate(driver)
        test_internet_pack_deactivate(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test_rate_plan()
