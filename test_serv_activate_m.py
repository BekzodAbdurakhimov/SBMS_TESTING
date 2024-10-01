import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

    add_packs_btn_locator = (By.CSS_SELECTOR, 'ps-button[title="Добавить пакет"] > ps-icon[icon="row-add"]')
    add_packs_btn = wait.until(EC.element_to_be_clickable(add_packs_btn_locator))
    add_packs_btn.click()

    # Открываем окно таблицы услуг
    packs_table_locator = (By.CSS_SELECTOR, 'table.n-grid.n-grid_checkable')
    wait.until(lambda driver: driver.find_element(*packs_table_locator).get_attribute("style") == "")
    print('Модальное окно услуги успешно загрузился')

    # Ишем TRAFFIC+
    pack_searcharea_locator = (By.CSS_SELECTOR, 'input.inp-text[ng-model="grd.filter.name"]')
    pack_searcharea = wait.until(EC.element_to_be_clickable(pack_searcharea_locator))
    pack_searcharea.send_keys(SERVICE_NAME)
    # pack_searcharea.send_keys('Data Pack 1 GB') # почему-то выбирает кто я))

    # Выбираем первый результат поиска
    td_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "td.n-grid__td.n-grid__select[data-column-index='1']"))
    )

    if td_elements:
        # Выбираем первый элемент
        first_td_element = td_elements[0]

        # Например, кликаем чекбокс внутри <td>
        checkbox_locator = first_td_element.find_element(By.CSS_SELECTOR, "span.n-check-checkbox")
        checkbox = wait.until(EC.element_to_be_clickable(checkbox_locator))
        checkbox.click()
        print("Чекбокс Пакеты успешно выбран.")
    else:
        print("Элементов не было найдено.")

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "tr.prop-list-table__row[ng-repeat-start='pack in packsData track by pack.packId']"))
    )
    print('Услуга Traffc+ выбран!')

    select_pack_locator = (By.XPATH, '//span[@class="b-button__label" and text()="Добавить"]')
    select_pack = wait.until(EC.element_to_be_clickable(select_pack_locator))
    select_pack.click()


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

    time.sleep(2)
    print('Успешно подключен пакет Traffic+!')
