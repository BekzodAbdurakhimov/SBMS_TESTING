from tests.test_rate_plan import test_rate_plan
from tests.test_serv_activate import test_serv_activate
from tests.test_serv_deactivate import test_serv_deactivate
from tests.test_sms_pack_activate import test_pack_activate
from tests.test_sms_pack_deactivate import test_pack_deactivate
from tests.test_internet_pack_activate import test_internet_pack_activate
from tests.test_internet_pack_deactivate import test_internet_pack_deactivate

from selenium import webdriver
import subprocess

def run_test_rate_plan():

    # Инициализация WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Вызов функций тестов
    try:
        test_rate_plan(driver)
        test_serv_activate(driver)
        test_serv_deactivate(driver)
        test_pack_activate(driver)
        test_pack_deactivate(driver)
        test_internet_pack_activate(driver)
        test_internet_pack_deactivate(driver)
        print("Все тесты выполнены успешно!")
    finally:
        driver.quit()

    # Вызываем скрипт для удаления файла с логином и паролем
    try:
        subprocess.run(["python", "delete_login_x_passwords.py"], check=True)
        print("Файл с логином и паролем успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

if __name__ == "__main__":
    run_test_rate_plan()
