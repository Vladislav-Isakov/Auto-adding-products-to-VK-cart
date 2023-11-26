import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    VK_USERNAME = os.environ.get('VK_USERNAME') or '' #логин VK аккаунта
    VK_PASSWORD = os.environ.get('VK_PASSWORD') or '' #пароль VK аккаунта
    VK_DOMAIN_LOGIN = os.environ.get('VK_DOMAIN_LOGIN') or '' #ссылка на адрес ВК регистрации, для входа в аккаунт