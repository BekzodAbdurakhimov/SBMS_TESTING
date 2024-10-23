from openpyxl import Workbook
import time
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.login_x_password import LOGIN, PASSWORD
from config.config import RATE_PLAN_NAME_1, RATE_PLAN_NAME_2

LOG_FILE = "../results/logs.txt"

def log_step(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}] {message}\n"
    print(log_message.strip())
    with open(LOG_FILE, "a") as file:
        file.write(log_message)

def test_sbms_open(driver):

    driver.get("https://sbms.ucell/ps/sbms/shell.html")
    wait = WebDriverWait(driver, 120)

    log_step(' ======== Смена ТП ========')

    # Проверка кнопки
    detail_button_check = wait.until(
        EC.visibility_of_element_located((By.ID, "details-button"))
    )
    detail_button_check.click()

    go_to_link = wait.until(
        EC.visibility_of_element_located((By.ID, "proceed-link"))
    )
    go_to_link.click()
    login_text_locator = (By.CSS_SELECTOR, '.login-caption > span')
    login_locator_check = wait.until(EC.visibility_of_element_located(login_text_locator))
    assert login_locator_check.is_displayed(), "Не найден локатор входа"

    # time.sleep(5)

    login_input_locator = (By.CSS_SELECTOR, "input.sbms-textbox[name='user'][type='text']")
    password_input_locator = (By.CSS_SELECTOR, "input.sbms-textbox[name='password'][type='password']")
    enter_btn_locator = (By.CSS_SELECTOR, "button.sbms-button-ex")

    # Ожидаем, пока поле ввода логина будет доступно для ввода
    login_input_area = wait.until(EC.element_to_be_clickable(login_input_locator))
    login_input_area.send_keys(LOGIN)

    # Ожидаем, пока поле ввода пароля будет доступно для ввода
    password_input_area = wait.until(EC.element_to_be_clickable(password_input_locator))
    password_input_area.send_keys(PASSWORD)

    # Ожидаем, пока кнопка "Войти" станет кликабельной
    enter_btn = wait.until(EC.element_to_be_clickable(enter_btn_locator))
    enter_btn.click()

    log_step('Вход в SBMS выполнен')

    # Ждать пока страничка не загрузиться полностью
    wait.until(
        lambda driver: "overflow: hidden; direction: ltr;" in driver.find_element(By.TAG_NAME,
                                                                                  "body").get_attribute(
            "style"))


    # Вход в витрину

