# -*- coding: UTF-8 -*-
from main import *

import passwords_obs
import functions_obs


__version__ = '0.10-01'


def add_new_resource(generic_key):
    """ Добавление нового ресурса """
    template_some_message(ACCENT_3, '||| ADD NEW RESOURCE |||')
    resource = input(ACCENT_1 + ' Resource: ' + ACCENT_4)
    login = input(ACCENT_1 + ' Login: ' + ACCENT_4)
    # Передача аргументов для выбора пароля
    passwords_obs.choice_generation_or_save_self_password(resource, login, generic_key)
    # Возвращение в лейбл по умолчанию
    functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
