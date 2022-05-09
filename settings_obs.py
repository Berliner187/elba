# -*- coding: UTF-8 -*-
from main import *
import category_actions_obs


__version__ = '0.9-10'


def settings(generic_key):
    write_log('Settings', 'Run')
    system_action('clear')
    cols = get_size_of_terminal()
    cols = cols - 1
    category = 'ELBA/SETTINGS'
    delta_category_len = (cols - (len('ELBA/SETTINGS') + 4)) // 2

    print(ACCENT_2, "\n", "|" * cols)
    print("", "|" * delta_category_len, GREEN, category, ACCENT_2, "|" * delta_category_len)
    print(ACCENT_2, "|" * cols, '\n' * 2)
    # Варианты настройки
    variation_settings = [
        'Customize Color Accent',
        'Manage Themes',
        'Optimization Program'
    ]
    cnt_variant = 0
    for variant in variation_settings:
        cnt_variant += 1
        print(f" {ACCENT_3}[{ACCENT_1}{cnt_variant}{ACCENT_3}] {ACCENT_1}{variant}{ACCENT_4}")

    def change_color_accent():
        """ Управление цветовыми акцентами """
        system_action('clear')
        # Выгрузка акцентов из файла
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
        setting_colors = int(template_input('Choose a color to change the accent:'))
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
        if setting_colors == 5:     # Костыль
            os.system(get_peculiarities_copy('rm') + FILE_SETTINGS_COLOR)
            system_action('clear')
            template_some_message(GREEN, '- Success -')
            sleep(1)

    def manage_themes():
        lines_themes = [
            "Light Theme",
            "Dark Theme"
        ]

        light_theme_default = {
            'ACCENT_1': '#FFFFFF',
            'ACCENT_2': '#FFFFFF',
            'ACCENT_3': '#FFFFFF',
            'ACCENT_4': '#000000',
        }
        dark_theme_default = {
            'ACCENT_1': '#FBC330',
            'ACCENT_2': '#9B30FF',
            'ACCENT_3': '#30A0E0',
            'ACCENT_4': '#FFFFFF'
        }

        def load_light_theme():
            create_file_with_theme(light_theme_default)

        def load_dark_theme():
            create_file_with_theme(dark_theme_default)

        dict_themes = {
            "1": load_light_theme,
            "2": load_dark_theme
        }

        # Прокрутка возможных действий
        print('\n')
        s = 0
        for theme in lines_themes:
            s += 1
            print(f" {ACCENT_3}[{ACCENT_1}{s}{ACCENT_3}] {ACCENT_1}{theme}{ACCENT_4}")

        user_change_theme = input(f"\n ELBA/SETTINGS/THEMES: ~$ {ACCENT_4}")
        try:
            dict_themes[user_change_theme]()
            system_action('restart')
        except KeyError:
            pass

    def optimisation():
        """ Оптимизация за счёт очистки кэша """
        template_remove_folder(get_peculiarities_system('rm_dir') + ' __pycache__/')
        system_action('clear')
        template_some_message(GREEN, "Success optimization")
        write_log("Delete cache", "QUIT")
        sleep(1)
        system_action('restart')

    actions_dict = {
        "1": change_color_accent,
        "2": manage_themes,
        "3": optimisation
    }

    # Выбор варианта настройки
    user_change = input('\n ELBA/SETTINGS: ~$ ')
    try:
        actions_dict[user_change]()
    except KeyError:
        pass
    # Возвращение в цикл decryption_block
    category_actions_obs.CategoryActions(generic_key, 'resource').get_category_label()
    write_log('Settings', 'Exit')
