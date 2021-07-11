from main import *

from enc_obs import *
from show_dec_data_obs import *
from del_resource_obs import delete_resource

from csv import DictReader, DictWriter
from time import sleep
from shutil import copyfile
import os


__version__ = '2.0.3'


def notes(generic_key):
    def add_new():  # Добавление новой заметки
        system_action('clear')
        print(BLUE + '    ---  Add new note  --- \n\n')
        name_note = input(YELLOW + ' - Name note: ' + DEFAULT_COLOR)
        note_itself = input(YELLOW + ' - Note: ' + DEFAULT_COLOR)
        save_data_to_file(name_note, note_itself, None, generic_key, 'note')
        print(GREEN, '   -- Success saved! --')
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
        delete_resource('note')
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
                    print(BLUE, data_type, YELLOW, dec_aes(value, generic_key), DEFAULT_COLOR)

                template_print_decryption_data(
                    'Note name ----->', name_note_from_file)
                template_print_decryption_data(
                    'Note itself --->', note_itself_from_file)
    notes(generic_key)
