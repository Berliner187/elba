from main import *
# Импорт переменных для работы с заметками
from csv import DictReader, DictWriter
from enc_obs import enc_data, dec_data
from time import sleep
from shutil import copyfile
import os


__version__ = '1.1.0'


def notes(master_password):
    system_action('clear')
    while True:     # Старт цикла для работы с заметками
        def show():     # Показ сохраненных заметок
            with open(FILE_FOR_NOTES, encoding='utf-8') as notes_file:
                reader_notes = DictReader(notes_file, delimiter=',')
                print(YELLOW + '       ---  Saved notes --- ', '\n' * 3 + DEFAULT_COLOR)
                number_note = 0     # Номер заметки
                for name in reader_notes:   # Перебор названий заметок
                    number_note += 1
                    dec_name_note = dec_data(name["name_note"], master_password)
                    # Вывод названий заметок и их порядкового номера
                    print(str(number_note) + '.', dec_name_note)
                print(BLUE + '\n  - Press "Enter" to go back'
                             '\n  - Enter "-a" to add new note'
                             '\n  - Enter "-d" to remove note',
                      YELLOW, '\n Select note by number', DEFAULT_COLOR)
        show()

        def add_new():  # Добавление новой заметки
            system_action('clear')
            print(BLUE + '    ---  Add new note  --- \n\n')
            with open(FILE_FOR_NOTES, mode="a", encoding='utf-8') as data_note:
                writer_note_add = DictWriter(data_note, fieldnames=fields_for_notes)
                name_note = input(YELLOW + ' - Note name: ' + DEFAULT_COLOR)
                note = input(PURPLE + ' - Note: ' + DEFAULT_COLOR)
                enc_name_note = enc_data(name_note, master_password)
                enc_note = enc_data(note, master_password)
                writer_note_add.writerow({
                    'name_note': enc_name_note,
                    'note': enc_note})
            print(green, '   -- Success saved! --')
            sleep(.3)
            system_action('clear')
            show()

        def work():     # Работа в лейбле с заметками
            change_action = input('\n - Change: ')  # Выбор между действиями
            if change_action == '-a':   # Пользователь выбирает добавление новой заметки
                add_new()
            elif change_action == '-d':  # Пользователь выбирает удаление старой заметки
                print(BLUE + '\n -- ' + 'Change by number note' + ' -- \n' + DEFAULT_COLOR)
                change_note_by_num = int(input(YELLOW + ' - Resource number: ' + DEFAULT_COLOR))
                # Выгрузка старого
                with open(FILE_FOR_NOTES, encoding='utf-8') as saved_note:
                    read_note = DictReader(saved_note, delimiter=',')
                    mas_name_note_rm, mas_note_rm = [], []
                    cnt_note = 0
                    for row_note in read_note:
                        cnt_note += 1
                        if cnt_note == change_note_by_num:
                            cnt_note += 1
                        else:  # Нужные ресурсы добавляются в массивы
                            mas_name_note_rm.append(row_note["name_note"])
                            mas_note_rm.append(row_note["note"])
                    saved_note.close()
                # Перенос в новый файл
                NEW_FILE_FOR_NOTES = 'new_note.dat'
                with open(new_FILE_FOR_NOTES, mode="a", encoding='utf-8') as new_notes:
                    write_note = DictWriter(new_notes, fieldnames=fields_for_notes)
                    for j in range(cnt_note-2):
                        write_note.writerow({
                            'name_note': mas_name_note_rm[j],
                            'note': mas_note_rm[j]})
                    new_notes.close()
                # Замена старого файла на актуальный
                copyfile(NEW_FILE_FOR_NOTES, FILE_FOR_NOTES)  # Старый записывается новым файлом
                os.system('rm ' + new_FILE_FOR_NOTES)  # Удаление нового файла
                system_action('clear')
                show()
            else:   # Вывод дешифрованных данных по выбранной цифре
                with open(FILE_FOR_NOTES, encoding='utf-8') as saved_note:  # Открытие в csv-формате
                    read_note = DictReader(saved_note, delimiter=',')   # Чтение библиоткой csv
                    count = 0   # Счетчик
                    for line_of_note in read_note:
                        count += 1
                        if count == int(change_action):  # Если счетчик совпадает с выбранным значением
                            system_action('clear')
                            show()  # Показываются сохраненные имена заметок
                            # Выводится зашифрованный вид выбранной заметки
                            print(YELLOW, '\n Name:', green,
                                  dec_data(line_of_note["name_note"], master_password), DEFAULT_COLOR,
                                  YELLOW, '\n Note:', green,
                                  dec_data(line_of_note["note"], master_password), DEFAULT_COLOR)
            work()  # Рекурсия
        work()  # Запуск
