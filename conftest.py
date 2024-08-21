import pytest
from selenium import webdriver


# test
@pytest.fixture(scope='function')
def driver():
    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Закрываем браузер после выполнения теста
    driver.quit()

