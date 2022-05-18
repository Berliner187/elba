# -*- coding: UTF-8 -*-
from main import *


__version__ = '0.9-10'


def settings():
    cols = get_size_of_terminal()
    cols = cols - 1
    category = 'ELBA/SETTINGS'

    # <<<<<<<<<<<<< ПЕРЕДЕЛАТЬ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def name_on_top():
        return f"||{GREEN} {category} "

    total_surface_length = "|" * (cols - 1)

    print(ACCENT_2, "\n", total_surface_length)  # 1 строка
    print(
        ACCENT_2, name_on_top() + ACCENT_3 + ('|' * (len(total_surface_length) - (len(category) + 4)))
    )  # 2 строка
    print(ACCENT_2, total_surface_length, "\n" * 2)  # 3 строка
    # <<<<<<<<<<<<<  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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

        # <<<<<<<<<<<<< ПЕРЕДЕЛАТЬ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def name_on_top():
            return f"||{GREEN} ELBA/SETTINGS/ACCENTS "

        total_surface_length = "|" * (cols - 1)

        print(ACCENT_2, "\n", total_surface_length)  # 1 строка
        print(
            ACCENT_2, name_on_top() + ACCENT_3 + ('|' * (len(total_surface_length) - (len(f'ELBA/SETTINGS/ACCENTS') + 4)))
        )  # 2 строка
        print(ACCENT_2, total_surface_length, "\n" * 2)  # 3 строка
        # <<<<<<<<<<<<<  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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
            print(f"{ACCENT_3}[{ACCENT_1}{cnt}{ACCENT_3}] "
                  f"{ACCENT_4}{item} = {format_hex_color(dic_colors[item])}"
                  f"{dic_colors[item]}")
        print(f"{ACCENT_3}[{ACCENT_1}{cnt + 1}{ACCENT_3}] {ACCENT_4}Set default color accent")

        template_some_message(ACCENT_3, '-- Color emphasis will change after restarting the program --')
        setting_colors = int(input(standard_location(ACCENT_4 + '/SETTINGS/ACCENTS')))
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
            "Dark Theme",
            "Green Theme",
            "Ocean Theme (Light)",
            "Coffee Theme"
        ]

        light_theme_default = {
            'ACCENT_1': '#FFFFFF',
            'ACCENT_2': '#FFFFFF',
            'ACCENT_3': '#FFFFFF',
            'ACCENT_4': '#000000',
            'ACCENT_5': '9B30FF'
        }
        dark_theme_default = {
            'ACCENT_1': '#595959',  # Основной №1
            'ACCENT_2': '#a5a5a5',  # Доп. цвет
            'ACCENT_3': '#cccccc',  # Основной №2
            'ACCENT_4': '#FFFFFF',
            'ACCENT_5': '9B30FF'
        }
        green_theme = {
            'ACCENT_1': '#cbef43',
            'ACCENT_2': '#8de969',
            'ACCENT_3': '#72a98f',
            'ACCENT_4': '#FFFFFF',
            'ACCENT_5': '9B30FF'
        }
        light_ocean_theme = {
            'ACCENT_1': '#2f4550',
            'ACCENT_2': '#2f4550',
            'ACCENT_3': '#586f7c',
            'ACCENT_4': '#000000',
            'ACCENT_5': '9B30FF'
        }
        coffee_theme = {
            'ACCENT_1': '#997d60',
            'ACCENT_2': '#bbbcbf',
            'ACCENT_3': '#bca58d',
            'ACCENT_4': '#e3d1df',
            'ACCENT_5': '9B30FF'
        }

        def load_light_theme():
            create_file_with_theme(light_theme_default)

        def load_dark_theme():
            create_file_with_theme(dark_theme_default)

        def load_green_theme():
            create_file_with_theme(green_theme)

        def load_light_ocean_theme():
            create_file_with_theme(light_ocean_theme)

        def load_coffee_theme():
            create_file_with_theme(coffee_theme)

        dict_themes = {
            "1": load_light_theme,
            "2": load_dark_theme,
            "3": load_green_theme,
            "4": load_light_ocean_theme,
            "5": load_coffee_theme
        }

        # Прокрутка возможных действий
        print('\n')
        cnt = 0
        for theme in lines_themes:
            cnt += 1
            print(f" {ACCENT_3}[{ACCENT_1}{cnt}{ACCENT_3}] {ACCENT_1}{theme}{ACCENT_4}")

        user_change_theme = input(standard_location('/SETTINGS/THEMES'))
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
    user_change = input(standard_location('/SETTINGS'))
    try:
        actions_dict[user_change]()
    except KeyError:
        pass
