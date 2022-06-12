from main import *

from security_obs import *
from functions_obs import ProgramFunctions
import functions_obs
import remove_obs
import control_bus_obs

from csv import DictReader, DictWriter
from time import sleep
import os


__version__ = '0.10-00'


def notes(generic_key):
    def add_new():  # Добавление новой заметки
        system_action('clear')
        template_some_message(ACCENT_3, '---  Add new note  ---')

        def add_non_empty_note():
            while True:
                _name_note = template_input('Name note:')
                _note_itself = template_input('Note:')
                if (_name_note or _note_itself) == '':
                    template_some_message(RED, 'Die Notiz darf nicht leer sein')
                else:
                    return _name_note, _note_itself

        name_note, note_itself = add_non_empty_note()
        save_data_to_file(name_note, note_itself, None, generic_key, 'note')
        template_some_message(GREEN, '--- Success saved! ---')
        sleep(.3)
        system_action('clear')
        ProgramFunctions(generic_key, 'note').get_category_label()
        notes(generic_key)

    if not(os.listdir(FOLDER_WITH_NOTES)):
        add_new()

    user_actions = input(standard_location('/NOTES'))  # Выбор между действиями

    if user_actions == '-a':   # Добавление новой заметки
        add_new()
    elif user_actions == '-d':  # Удаление имеющийся заметки
        remove_obs.Remove(generic_key, 'note').remove_object()
        ProgramFunctions(generic_key, 'note').get_category_label()
        notes(generic_key)
    elif user_actions == '-x':
        quit()
    elif user_actions.isnumeric():  # Отображение сохраненных данных о ресурсе
        system_action('clear')
        user_actions = int(user_actions)
        system_action('clear')
        ProgramFunctions(generic_key, 'note').get_category_label()

        path_to_note = FOLDER_WITH_NOTES + os.listdir(FOLDER_WITH_NOTES)[user_actions-1]
        template_print_decryption_data(
            'Name', f"{path_to_note}/{FILE_NOTE_NAME}", generic_key)
        template_print_decryption_data(
            'Note', f"{path_to_note}/{FILE_NOTE_ITSELF}", generic_key)

    else:
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
        control_bus_obs.control_bus(generic_key)
    notes(generic_key)
