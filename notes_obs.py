from main import *

from enc_obs import *
from show_dec_data_obs import *
from del_object_obs import delete_object

from csv import DictReader, DictWriter
from time import sleep
from shutil import copyfile
import os


__version__ = 'P8.6_M1.0'


def notes(generic_key):
    def add_new():  # Добавление новой заметки
        system_action('clear')
        template_some_message(ACCENT_3, '  ---  Add new note  ---')
        name_note = input(ACCENT_1 + ' - Name note: ' + ACCENT_4)
        note_itself = input(ACCENT_1 + ' - Note: ' + ACCENT_4)
        save_data_to_file(name_note, note_itself, None, generic_key, 'note')
        template_some_message(GREEN, '   -- Success saved! --')
        sleep(.3)
        system_action('clear')
        show_decryption_data(generic_key, 'note')
        notes(generic_key)

    if not(os.listdir(FOLDER_WITH_NOTES)):
        add_new()

    change_action = input('\n - Change action: ')  # Выбор между действиями

    if change_action == '-a':   # Пользователь выбирает добавление новой заметки
        add_new()
    elif change_action == '-d':  # Пользователь выбирает удаление старой заметки
        delete_object('note')
        show_decryption_data(generic_key, 'note')
        notes(generic_key)
    elif change_action == '-x':
        quit()
    else:
        cnt = 0
        for note_in_folder in os.listdir(FOLDER_WITH_NOTES):
            cnt += 1
            if cnt == int(change_action):
                system_action('clear')
                show_decryption_data(generic_key, 'note')

                path_to_note = FOLDER_WITH_NOTES + note_in_folder
                name_note_from_file = path_to_note + '/' + FILE_NOTE_NAME
                note_itself_from_file = path_to_note + '/' + FILE_NOTE_ITSELF

                def template_print_decryption_data(data_type, value):
                    print(ACCENT_3, data_type, ACCENT_1, dec_aes(value, generic_key), ACCENT_4)

                template_print_decryption_data(
                    'Note name ----->', name_note_from_file)
                template_print_decryption_data(
                    'Note itself --->', note_itself_from_file)
    notes(generic_key)
