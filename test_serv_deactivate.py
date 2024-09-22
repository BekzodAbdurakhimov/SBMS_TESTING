import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import LOGIN, PASSWORD, PACKAGE_NAME, RATE_PLAN_NAME, SERVICE_NAME, PHONE_NUM


def test_login_account(driver):
    driver.get("https://sbms.ucell/ps/sbms/shell.html")
    wait = WebDriverWait(driver, 120)

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

    print('Вход в SBMS выполнен')

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

    print('Витрина абонента открыта')

    # Ввод MSISDN
    input_tel_number_locator = (By.CLASS_NAME, "inp-text")
    input_tel_number = wait.until(EC.element_to_be_clickable(input_tel_number_locator))
    input_tel_number.send_keys("998501041717")
    # time.sleep(5)

    print('MSISDN введен')

    # Клик по кнопке ПОИСК
    search_elements_locator = (By.CSS_SELECTOR, 'ps-icon[icon="search-white"]')
    search_elements = wait.until(EC.element_to_be_clickable(search_elements_locator))
    search_elements.click()
    # time.sleep(5)

    approve_num_btn_locator = (By.XPATH, "//span[@class='b-button__label' and text()='Да']/..")
    approve_num_btn = wait.until(EC.element_to_be_clickable(approve_num_btn_locator))
    approve_num_btn.click()
    # time.sleep(5)

    print('Поиск выполнен и номер подтвержден')

    balance_of_subs_before = (By.CSS_SELECTOR, 'span#ps_customer_subscriber_summary_common_balance')
    wait.until(EC.element_to_be_clickable(balance_of_subs_before))
    balance_before_activating_rate_plan = driver.find_element(By.CSS_SELECTOR,
                                                              'span#ps_customer_subscriber_summary_common_balance')
    balance_before_activating_rate_plan_text = \
        balance_before_activating_rate_plan.text.replace('UZS', '').strip().replace(' ', '').split('.')[0]
    print(f'Баланс до подключения ТП: {int(balance_before_activating_rate_plan_text)}')

    # ============================= ТЕСТИРОВАНИЕ УСЛУГИ НАЧИНАЕТСЯ ЗДЕСЬ =============================

    clients_btn_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Клиенты"]')
    clients_btn = wait.until(EC.element_to_be_clickable(clients_btn_locator))
    clients_btn.click()

    abonents_btn_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Абоненты"]')
    abonents_btn = wait.until(EC.element_to_be_clickable(abonents_btn_locator))
    abonents_btn.click()

    services_cathegory_btn_locator = (By.XPATH, '//a[@class="menu__a-vertical" and text()="Услуги"]')
    services_cathegory_btn = wait.until(EC.element_to_be_clickable(services_cathegory_btn_locator))
    services_cathegory_btn.click()

    """ 
    ============================================= РАЗДЕЛ УСЛУГИ ==================================================
    """

    packs_btn_locator = (By.XPATH, '//a[@class="n-tab__title" and text()="Пакеты"]')
    packs_btn = wait.until(EC.element_to_be_clickable(packs_btn_locator))
    packs_btn.click()

    """ ============================================= HERE GOES DEACTIVATING THE SERVICE ============================================= """

    serv_search_input_clear_locator = (By.XPATH,
                                                  "//input[@ng-model='grdPacks.filter.name' and contains(@class, 'inp-text')]")
    serv_search_input_clear = wait.until(EC.element_to_be_clickable(serv_search_input_clear_locator))
    clear_input_action = ActionChains(driver)
    clear_input_action.double_click(serv_search_input_clear).perform()
    # input_element.send_keys(Keys.CONTROL, 'a')
    time.sleep(2)
    serv_search_input_clear.send_keys(Keys.BACKSPACE)
    time.sleep(2)

    serv_search_input_locator = (By.XPATH,
                                            "//input[@ng-model='grdPacks.filter.name' and contains(@class, 'inp-text')]")
    serv_search_input = wait.until(EC.element_to_be_clickable(serv_search_input_locator))
    serv_search_input.send_keys('Traffic')

    serv_state_click_locator = (By.XPATH, '//div[@class="n-grid-title-in" and @style="z-index: 8;"]')
    serv_state_click = wait.until(EC.element_to_be_clickable(serv_state_click_locator))
    serv_state_click.click()

    serv_search_input.click()

    delete_serv_btn_locator = (By.CSS_SELECTOR,
                                          'ps-button[title="Отключить пакет"] > ps-icon[icon="row-delete"]')
    delete_serv_btn = wait.until(EC.element_to_be_clickable(delete_serv_btn_locator))
    delete_serv_btn.click()

    serv_comment_input_locator = (By.XPATH, '//input[@ng-model="deactivateServices.deleteComment"]')
    serv_comment_input = wait.until(EC.element_to_be_clickable(serv_comment_input_locator))
    serv_comment_input.send_keys('TEST')

    serv_deactivate_btn_locator = (By.XPATH, '//span[@class="b-button__label" and text()="Отключить"]')
    serv_deactivate_btn = wait.until(EC.element_to_be_clickable(serv_deactivate_btn_locator))
    serv_deactivate_btn.click()

    # wait till the update btn gets available
    """ ============================================= IT ENDS HERE ============================================= """

    # refreshing the page 3 times to make sure that the Pack has been activated
    refresh_btn = driver.find_element(By.XPATH, '//ps-button[@ng-click="updateBalances();"]')
    for _ in range(3):
        refresh_btn.click()
        time.sleep(10)
    print('Кнопка обновить был нажат 3 раза в течение 30 секунды')

    balance_of_subs_after = (By.CSS_SELECTOR, 'span#ps_customer_subscriber_summary_common_balance')
    wait.until(EC.element_to_be_clickable(balance_of_subs_after))
    balance_after_activating_rate_plan = driver.find_element(By.CSS_SELECTOR,
                                                             'span#ps_customer_subscriber_summary_common_balance')
    balance_after_activating_rate_plan_text = \
        balance_after_activating_rate_plan.text.replace('UZS', '').strip().replace(' ', '').split('.')[0]
    print(f'Баланс после подключения ТП: {int(balance_after_activating_rate_plan_text)}')

    time.sleep(5)
    print('Успешно отключен пакет Traffic+!')
