from dotenv import dotenv_values

config = {
    **dotenv_values(".env")
}
class Config(object):
    VK_USERNAME = config.get('VK_USERNAME', None) #логин VK аккаунта
    VK_PASSWORD = config.get('VK_PASSWORD', None) #пароль VK аккаунта
    VK_DOMAIN_LOGIN = config.get('VK_DOMAIN_LOGIN', None) #ссылка на адрес ВК регистрации, для входа в аккаунт
    VK_DOMAIN_GROUP = config.get('VK_DOMAIN_GROUP', None) #ссылка на продукт в магазине группы в ВК, в которой есть магазин
    VK_DOMAIN_GROUP_2 = config.get('VK_DOMAIN_GROUP_2', None) # ссылка на корзину данной группы
    DELIVERRY_ADDRESS = config.get('DELIVERRY_ADDRESS', None) # адрес для доставки заказа, данный адрес будет вставлен в поле адреса при оформлении заказа
    DELIVERRY_PERSON = config.get('DELIVERRY_PERSON', None) # ФИО получателя товара
    VK_BACKUP_CODES = config.get('VK_BACKUP_CODES', None) # строка с массивом, из чисел=резервных кодов 