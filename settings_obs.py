# -*- coding: UTF-8 -*-
from main import *
import category_actions_obs


__version__ = '0.9-01'


def settings(generic_key):
    system_action('clear')
    write_log('Settings', 'Run')
    template_some_message(GREEN, '--- Settings ---')
    # Варианты настройки
    variation_settings = [
        'Customize colors accent',
        'Optimization program'
    ]
    cnt_variant = 0
    for variant in variation_settings:
        cnt_variant += 1
        print(f'{ACCENT_3}{cnt_variant}. {ACCENT_1}{variant}')

    # Выбор варианта настройки
    change_in_settings = input('\n - Change setting by number: ')
    # Первый вариант
    if change_in_settings == '1':
        system_action('clear')

        dic_colors = ''
        with open(FILE_SETTINGS_COLOR, 'r') as f:
            for i in f.readlines():
                dic_colors = i
        dic_colors = eval(dic_colors)

        # Показ настроек, которые возможны
        cnt = 0
        for item in dic_colors:
            cnt += 1
            print(f"{ACCENT_1}{cnt}. "
                  f"{ACCENT_4}{item} = {format_hex_color(dic_colors[item])}"
                  f"{dic_colors[item]}")
        print(f"{ACCENT_1}{cnt + 1}. {ACCENT_4}Set default color accent")

        template_some_message(ACCENT_3, '-- Color emphasis will change after restarting the program --')
        setting_colors = int(input(ACCENT_1 + ' - Choose a color to change the accent: '))
        cnt = 0
        # Прокрутка до нужной настройки
        for select in dic_colors:
            cnt += 1
            # Кастомизация цвета
            if setting_colors == cnt:
                while True:
                    new_color = input(f'{GREEN} - Input new color in HEX: {ACCENT_4}#')
                    if len(new_color) == 6:
                        break
                    else:
                        template_some_message(RED, '- HEX format should consist of 6 characters -')
                dic_colors[select] = f'#{new_color}'.upper()
                with open(FILE_SETTINGS_COLOR, 'w+') as file_colors:
                    file_colors.write(str(dic_colors))
                    file_colors.close()
                system_action('clear')
                template_some_message(GREEN, '- Successfully changed color accent -')
                sleep(1)
        if setting_colors == 5:
            os.system(get_peculiarities_copy('rm') + FILE_SETTINGS_COLOR)
            system_action('clear')
            template_some_message(GREEN, '- Success -')
            sleep(1)
    # Второй вариант
    elif change_in_settings == '2':
        # Оптимизация за счёт удаления лишнего кэша модулей
        template_remove_folder('rm -r __pycache__/')
        system_action('clear')
        template_some_message(GREEN, "Success optimization")
        write_log("Delete cache", "QUIT")
        sleep(1)
        system_action('restart')
    category_actions_obs.CategoryActions(generic_key, 'resource').get_category_label()
    write_log('Settings', 'Run')
