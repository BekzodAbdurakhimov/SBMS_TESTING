# from openpyxl import Workbook
import time
from datetime import datetime
# from openpyxl.reader.excel import load_workbook

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import LOGIN, PASSWORD, PHONE_NUM

LOG_FILE = "logs.txt"
EXCEL_FILE = "SBMS_AUTOTEST_RESULTS.xlsx"

def log_step(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}] {message}\n"
    print(log_message.strip())
    with open(LOG_FILE, "a") as file:
        file.write(log_message)

def test_func_sbms(driver):
    # global wb, ws
    #
    # # Попробуйте открыть существующий файл или создать новый
    # try:
    #     wb = load_workbook(EXCEL_FILE)
    #     ws = wb.active
    # except FileNotFoundError:
    #     wb = Workbook()
    #     ws = wb.active

    driver.get("https://sbms.ucell/ps/sbms/shell.html")
    wait = WebDriverWait(driver, 120)

    log_step(' ======== Подключение Услуги ========')

    # # Проверка кнопки
    # detail_button_check = wait.until(
    #     EC.visibility_of_element_located((By.ID, "details-button"))
    # )
    # detail_button_check.click()
    #
    # go_to_link = wait.until(
    #     EC.visibility_of_element_located((By.ID, "proceed-link"))
    # )
    # go_to_link.click()
    # login_text_locator = (By.CSS_SELECTOR, '.login-caption > span')
    # login_locator_check = wait.until(EC.visibility_of_element_located(login_text_locator))
    # assert login_locator_check.is_displayed(), "Не найден локатор входа"

    """ ========================================== Запуск SBMS ========================================== """

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

    # Локаторы для элементов меню
    cabs_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Витрины"]')
    subs_cabinet_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Витрина абонента"]')

    # Ожидание кликабельности элемента "Витрины" и клик по нему
    cabs = wait.until(EC.element_to_be_clickable(cabs_locator))
    cabs.click()

    # Ожидание кликабельности элемента "Витрина абонента" и клик по нему
    subs_cabinet = wait.until(EC.element_to_be_clickable(subs_cabinet_locator))
    subs_cabinet.click()

    wait.until(
        lambda driver: "overflow: hidden; direction: ltr;" in driver.find_element(By.TAG_NAME, "body").get_attribute(
            "style"))

    log_step('Витрина абонента открыта')
    log_step("Запуск SBMS DONE")
    """ ===================== Поиск клиента ===================== """

    search_client_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Клиенты"]')
    search_client = wait.until(EC.element_to_be_clickable(search_client_locator))
    search_client.click()
    log_step('Открытие пунтка Клиенты')

    clients_btn_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Поиск / выбор клиента"]')
    clients_btn = wait.until(EC.element_to_be_clickable(clients_btn_locator))
    clients_btn.click()

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "fr3")))

    search_num_locator = (By.CSS_SELECTOR, 'input#MSISDN.sbms-textbox')
    search_num = wait.until(EC.presence_of_element_located(search_num_locator))
    search_num.send_keys(PHONE_NUM)


    search_client_btn_locator = (By.XPATH, '//td[@class="sbms-btn-label-ex" and text()="Поиск"]')
    search_client_btn = wait.until(EC.element_to_be_clickable(search_client_btn_locator))
    search_client_btn.click()
    log_step('Поиск клиента DONE')

    """ ========================================== Отображение данные КЛИЕНТА на карточке клиента ========================================== """

    tab_holder_locator = (By.ID, "TAB_HOLDER_3")
    wait.until(EC.visibility_of_element_located(tab_holder_locator))
    log_step('Отображение данные КЛИЕНТА DONE')

    """ ========================================== Синхронизация баланса BIS с BRT ========================================== """
    time.sleep(2)

    input_field_locator = (By.ID, 'txtUBLNC')
    input_field = wait.until(EC.element_to_be_clickable(input_field_locator))
    value = input_field.get_attribute('value')

    # Извлечение числовой части и формирование строки для OCS
    clean_value = value.split(' ')[0].split('.')[0]
    balance_ocs = int(clean_value)  # Преобразуем в целое число

    driver.switch_to.default_content()

    # Ожидание и получение баланса из OCS
    balance_of_subs_before = (By.CSS_SELECTOR, 'span#ps_customer_subscriber_summary_common_balance')
    wait.until(EC.element_to_be_clickable(balance_of_subs_before))
    balance_before_test = driver.find_element(By.CSS_SELECTOR, 'span#ps_customer_subscriber_summary_common_balance')
    balance_before_test = balance_before_test.text.replace('UZS', '').strip().replace(' ', '').split('.')[0]
    balance_bis = int(balance_before_test)  # Преобразуем в целое число

    # Проверка равенства с использованием assert
    if balance_ocs == balance_bis:
        log_step(f"Балансы совпадают! DONE: BIS:{balance_bis} | OCS:{balance_ocs}")
    else:
        assert False, f"Балансы не совпадают: FAIL BIS = {balance_ocs}, OCS = {balance_bis}"

    """ ========================================== «Фин. карточка клиента»  ========================================== """

    search_fincard_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Фин. карточка клиента"]')
    search_fincard = wait.until(EC.element_to_be_clickable(search_fincard_locator))
    search_fincard.click()
    log_step('Открытие пунтка Фин. карточка клиента')

    time.sleep(2)

    # Платежи
    payments_item_area_locator = (By.CSS_SELECTOR, 'div[ng-controller="customerPayments"][name="customerPayments"]')
    wait.until(EC.visibility_of_element_located(payments_item_area_locator))
    log_step('Пункт "Платежи" отображается | Фин. карточка')

    # Корректировки
    adjustments_item_locator = (By.CSS_SELECTOR, 'li[ng-repeat="(key, tab) in tabs track by tab.$id"][title="Корректировки платежей и начислений на лицевом счете клиента"]')
    adjustments_item = wait.until(EC.element_to_be_clickable(adjustments_item_locator))
    adjustments_item.click()

    adjustments_item_area_locator = (By.CSS_SELECTOR, 'div[ng-controller="customerAdjustments"][name="customerAdjustments"][ps-dialog-controller="customerAdjustments"].b-form-container.b-form-container_full_size')
    wait.until(EC.visibility_of_element_located(adjustments_item_area_locator))
    log_step('Пункт "Корректировки" отображается | Фин. карточка')

    # Счета
    bills_item_locator = (By.CSS_SELECTOR, 'li[ng-repeat="(key, tab) in tabs track by tab.$id"][title="Биллинговые счета клиента"]')
    bills_item = wait.until(EC.element_to_be_clickable(bills_item_locator))
    bills_item.click()

    bills_item_area_locator = (By.CSS_SELECTOR, 'div[ng-controller="customerBills"][name="customerBills"][ps-dialog-controller="customerBills"]')
    wait.until(EC.visibility_of_element_located(bills_item_area_locator))
    log_step('Пункт "Счета" отображается | Фин. карточка')

    # История баланса
    balance_hist_item_locator = (By.CSS_SELECTOR, 'li[ng-repeat="(key, tab) in tabs track by tab.$id"][title="История баланса"]')
    balance_hist_item = wait.until(EC.element_to_be_clickable(balance_hist_item_locator))
    balance_hist_item.click()

    balance_hist_item_area_locator = (By.CSS_SELECTOR, 'div[ng-controller="balanceHistory"][name="balanceHistory"].b-form-container.b-form-container_full_size.b-form-container_with_padding')
    wait.until(EC.visibility_of_element_located(balance_hist_item_area_locator))
    log_step('Пункт "История баланса" отображается | Фин. карточка')

    # Обещанные платежи
    promised_payment_item_locator = (By.CSS_SELECTOR, 'li[ng-repeat="(key, tab) in tabs track by tab.$id"][title="Обещанные платежи"]')
    promised_payment_item = wait.until(EC.element_to_be_clickable(promised_payment_item_locator))
    promised_payment_item.click()

    promised_payment_item_area_locator = (By.CSS_SELECTOR, 'ps-tab[caption="Обещанные платежи"].tabbed-content__item')
    wait.until(EC.visibility_of_element_located(promised_payment_item_area_locator))
    log_step('Пункт "Обещанные платежи" отображается | Фин. карточка')

    # Расширенная история баланса
    extended_balance_hist_item_locator = (By.CSS_SELECTOR, 'li[ng-repeat="(key, tab) in tabs track by tab.$id"][title="Расширенная история баланса"]')
    extended_balance_hist_item = wait.until(EC.element_to_be_clickable(extended_balance_hist_item_locator))
    extended_balance_hist_item.click()

    extended_balance_hist_item_area_locator = (By.CSS_SELECTOR, 'ps-splitter[ng-if*="context.hasNoBilling"].ps-splitter.ui-splitter.ui-splitter-horizontal')
    wait.until(EC.visibility_of_element_located(extended_balance_hist_item_area_locator))
    log_step('Пункт "Расширенная история баланса" отображается | Фин. карточка')

    """ ========================================== «Поиск абонента»  ========================================== """

    # Витрина абонента
    search_vitrina_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Витрина абонента"]')
    search_vitrina = wait.until(EC.element_to_be_clickable(search_vitrina_locator))
    search_vitrina.click()
    log_step('Открытие пунтка Витрина абонента')

    search_btn_locator = (By.XPATH, "//ps-button[@id='ps_customer_subscriber_summary_search' and @icon='search' and contains(@class, 'subscriber-summary-box_search-button')]")
    search_btn = wait.until(EC.element_to_be_clickable(search_btn_locator))
    search_btn.click()

    # Ввод MSISDN
    input_tel_number_locator = (By.CLASS_NAME, "inp-text")
    input_tel_number = wait.until(EC.element_to_be_clickable(input_tel_number_locator))
    input_tel_number.send_keys(PHONE_NUM)
    # time.sleep(5)
    log_step('MSISDN введен')

    # Клик по кнопке ПОИСК
    search_elements_locator = (By.CSS_SELECTOR, 'ps-icon[icon="search-white"]')
    search_elements = wait.until(EC.element_to_be_clickable(search_elements_locator))
    search_elements.click()

    approve_num_btn_locator = (By.XPATH, "//span[@class='b-button__label' and text()='Да']/..")
    approve_num_btn = wait.until(EC.element_to_be_clickable(approve_num_btn_locator))
    approve_num_btn.click()

    log_step('success')
    time.sleep(2)