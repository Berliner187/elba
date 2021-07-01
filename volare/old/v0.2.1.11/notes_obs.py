from main import *

from enc_obs import *
from del_resource import delete_resource

from csv import DictReader, DictWriter
from time import sleep
from shutil import copyfile
import os


__version__ = '2.0.0 ON DEVELOPMENT STAGE'


def notes(master_password):
    system_action('clear')
    show_decryption_data(master_password, 'note')

    while True:     # Старт цикла для работы с заметками

        def add_new():  # Добавление новой заметки
            system_action('clear')
            print(BLUE + '    ---  Add new note  --- \n\n')
            name_note = 'Test Name Note'
            print(name_note)
            note_itself = 'Test Note smth...'
            print(note_itself)
            sleep(.5)
            save_data_to_file(name_note, note_itself, None, master_password, 'note')
            print(GREEN, '   -- Success saved! --')
            sleep(.3)
            system_action('clear')

        def launcher_notes():     # Работа в лейбле с заметками
            change_action = input('\n - Change: ')  # Выбор между действиями
            if change_action == '-a':   # Пользователь выбирает добавление новой заметки
                add_new()
            elif change_action == '-d':  # Пользователь выбирает удаление старой заметки
                print(BLUE + '\n -- ' + 'Change by number note' + ' -- \n' + DEFAULT_COLOR)
                change_note_by_num = int(input(YELLOW + ' - Resource number: ' + DEFAULT_COLOR))
                delete_resource('note')

            cnt = 0
            for note_in_folder in os.listdir(FOLDER_WITH_NOTES):
                cnt += 1
                if cnt == int(change_action):
                    system_action('clear')
                    show_decryption_data(master_password, 'note')

                    path_to_note = FOLDER_WITH_NOTES + note_in_folder
                    name_note_from_file = path_to_note + '/' + FILE_NOTE_NAME
                    note_itself_from_file = path_to_note + '/' + FILE_NOTE_ITSELF

                    def template_print_decryption_data(data_type, value):
                        print(BLUE, data_type, YELLOW, dec_aes(value, master_password), DEFAULT_COLOR)

                    template_print_decryption_data(
                        'Name note --->', name_note_from_file)
                    template_print_decryption_data(
                        'Note itself --->', note_itself_from_file)

        launcher_notes()
