import ast
from pprint import pprint as print
from config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


username = Config.VK_USERNAME # логин аккаунта ВК
password = Config.VK_PASSWORD # пароль аккаунта ВК
delivery_address = Config.DELIVERRY_ADDRESS # адрес доставки товара
delivery_person = Config.DELIVERRY_PERSON # ФИО получателя товара

# Инициализация драйвера FireFox
driver = webdriver.Firefox()

# переход на страницу входа в VK
driver.get(Config.VK_DOMAIN_LOGIN)

# словарь с одноразовыми резервными кодами для входа в аккаунт
# получается по адресу: https://id.vk.com/account/#/reserve-codes
cods = {i*2: i for i in ast.literal_eval(Config.VK_BACKUP_CODES)}

# найти поле имени пользователя / электронной почты и отправить сам логин пользователя в поле ввода
# после ввода нажатие на кнопку входа и ожидание инициализации JS кода на фронте - implicitly_wait(parametr - секунды)
driver.find_element(By.ID, 'index_email').send_keys(username)
driver.find_element(By.CLASS_NAME, 'VkIdForm__signInButton').click()
driver.implicitly_wait(2)

# нажатие на кнопку входа другим способом(т.к. необходимо входить в аккаунт по резервным кодам, минуя двухфакторку)
driver.find_element(By.CSS_SELECTOR, 'button.vkc__ConfirmOTP__button').click()
driver.implicitly_wait(2)

# нажатие на кнопку резервный код
driver.find_elements(By.CLASS_NAME, "vkuiSimpleCell")[4].click()
error_message = 'Incorrect code'

# перебор резервных кодов из словаря cods, в случае если код уже ранее использован
# вводится следующий код, пока не будет введёный активный код
for cod in cods.values():

    # поиск и ввод в input резервного кода
    driver.find_element(By.ID, 'otp').send_keys(cod)
    driver.find_element(By.CLASS_NAME, 'vkc__ConfirmOTP__buttonSubmit').click()
    driver.implicitly_wait(1)

    # поиск текста ошибки, если резервный код уже недействительный
    # если код не действительный, задержка в секунду(чтобы не словить капчу из-за кол-во запросов к API)
    # и ввод следующего резервного кода из словаря cods
    errors = driver.find_elements(By.CLASS_NAME, 'vkc__TextField__errorMessage')
    if any(error_message in e.text for e in errors):
        time.sleep(1)
        continue
    break

# поиск и ввод пароля от аккаунта
driver.find_element(By.NAME, 'password').send_keys(password)
driver.implicitly_wait(1)

# нажатие на кнопку входа в аккаунт
driver.find_element(By.CLASS_NAME, 'vkuiButton--lvl-primary').click()
driver.implicitly_wait(7)

# поиск и нажатие на кнопку перехода в раздел со списком групп
driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/nav/ol/li[6]/a").click()
driver.implicitly_wait(10)

# поиск и нажатие на первую группу в списке ранее просмотренных групп 
driver.find_element(By.XPATH, "/html/body/div[11]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[1]/div/section/div[2]/div/div/div/div/div[2]/a").click()
driver.implicitly_wait(10)

# поиск и нажатие на товар в группе
driver.find_element(By.XPATH, "/html/body/div[11]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/section/div/ul/li[1]/div/a/div[1]/a").click()
driver.implicitly_wait(10)

# поиск и нажатие на кнопку добавления товара в корзину
driver.find_element(By.CLASS_NAME, 'ButtonAddToCart__addToCart').click()
driver.implicitly_wait(2)

while True:
    try:
        errors_in_group = driver.find_element(By.XPATH, '/html/body/div[23]/div/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[3]/div/div/button/span/span').get_attribute("innerHTML")
        if 'Добавлено в корзину (1)' not in errors_in_group and 'Добавлено в корзину ' not in errors_in_group and 'Добавлено в корзину' not in errors_in_group and 'В корзине' not in errors_in_group:
            driver.find_element(By.CLASS_NAME, 'ButtonAddToCart__addToCart').click()
            print('Block')
            time.sleep(5)
            continue
    except:
        pass

    # переход на страницу с корзиной в группе
    driver.get(Config.VK_DOMAIN_GROUP_2)
    driver.implicitly_wait(1)

    # нажатие на селектор с выбором способа доставки
    driver.find_element(By.CLASS_NAME, 'selector_input').click()
    driver.implicitly_wait(2)

    # выбор параметра доставки по почте из селектора способа доставки
    driver.find_element(By.XPATH, '//*[@id="option_list_options_container_2_3"]').click()
    driver.implicitly_wait(2)

    # ввод данных адреса для доставки
    driver.find_element(By.ID, 'market_cart_delivery_address').send_keys(delivery_address)

    # удаление и вставка ФИО получателя для доставки
    driver.find_element(By.ID, 'market_cart_delivery_person').clear()
    driver.find_element(By.ID, 'market_cart_delivery_person').send_keys(delivery_person)

    # нажатие на кнопку оформления заказа и завершение цикла
    driver.find_element(By.ID, 'market_shop_create_order').click()
    break