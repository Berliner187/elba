# -*- coding: UTF-8 -*-
from main import *

from passwords_obs import creating_new_password
from functions_obs import ProgramFunctions


__version__ = '0.10-02'


def add_new_resource(generic_key):
    """ Добавление нового ресурса (сервиса) """
    template_some_message(ACCENT_3, '--- ADD NEW SERVICE ---')
    service = input(ACCENT_1 + ' Service: ' + ACCENT_4)
    login = input(ACCENT_1 + ' Login: ' + ACCENT_4)
    # Передача аргументов для выбора пароля
    creating_new_password(service, login, generic_key)
    # Возвращение в лейбл по умолчанию
    ProgramFunctions(generic_key, 'resource').get_category_label()
