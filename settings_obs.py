# -*- coding: UTF-8 -*-
from main import *
import random
import getpass
import functions_obs


__version__ = '0.10-02'


cols = get_size_of_terminal()


def settings():
    category = 'SETTINGS'
    functions_obs.StylishLook().topper(category)

    # Варианты настройки
    variation_settings = [
        'Customize Color Accent',
        'Manage Themes',
        'Optimization Program'
    ]
    functions_obs.StylishLook().scrolling_and_numbering_content(variation_settings)

    def change_color_accent():
        """ Управление цветовыми акцентами """
        system_action('clear')
        accents_location = f"{category}/ACCENTS"

        functions_obs.StylishLook().topper(accents_location)

        # Выгрузка акцентов из файла
        accents_from_file = ''
        with open(FILE_SETTINGS_COLOR, 'r') as f:
            for i in f.readlines():
                accents_from_file = i
        accents_from_file = eval(accents_from_file)

        # Показ настроек, которые возможны
        cnt = 0
        for item in accents_from_file:
            cnt += 1
            print(f"{ACCENT_3}[{ACCENT_1}{cnt}{ACCENT_3}] "
                  f"{ACCENT_4}{item} = {format_hex_color(accents_from_file[item])}"
                  f"{accents_from_file[item]}")
        print(f"{ACCENT_3}[{ACCENT_1}{cnt + 1}{ACCENT_3}] {ACCENT_4}Set default color accent")

        template_some_message(ACCENT_3, '-- Color emphasis will change after restarting the program --')
        setting_colors = int(input(standard_location(ACCENT_4 + accents_location)))
        cnt = 0
        # Прокрутка до нужной настройки
        for select in accents_from_file:
            cnt += 1
            # Кастомизация цвета
            if setting_colors == cnt:
                while True:
                    new_color = input(f'{GREEN} - Input new color in HEX: {ACCENT_4}#')
                    if len(new_color) == 6:
                        break
                    else:
                        template_some_message(RED, '- HEX format should consist of 6 characters -')
                accents_from_file[select] = f'#{new_color}'.upper()
                with open(FILE_SETTINGS_COLOR, 'w+') as file_colors:
                    file_colors.write(str(accents_from_file))
                    file_colors.close()
                system_action('clear')
                template_some_message(GREEN, '- Successfully changed color accent -')
                sleep(1)
        if setting_colors == 6:     # Костыль
            os.system(get_peculiarities_copy('rm') + FILE_SETTINGS_COLOR)
            system_action('clear')
            template_some_message(GREEN, '- Success -')
            sleep(1)

    def manage_themes():
        """ Управление темами """
        system_action('clear')
        themes_location = f"{category}/THEMES"
        functions_obs.StylishLook().topper(themes_location)

        light_theme_default = {
            'ACCENT_1': '#FFFFFF',
            'ACCENT_2': '#FFFFFF',
            'ACCENT_3': '#FFFFFF',
            'ACCENT_4': '#000000',
            'ACCENT_5': '9B30FF'
        }
        strawberry_theme = {
            'ACCENT_1': '#FFCDAA',
            'ACCENT_2': '#9CB898',
            'ACCENT_3': '#EE8980',
            'ACCENT_4': '#FFFFFF',
            'ACCENT_5': '#B588F7'
        }
        green_theme = {
            'ACCENT_1': '#cbef43',
            'ACCENT_2': '#8de969',
            'ACCENT_3': '#72a98f',
            'ACCENT_4': '#FFFFFF',
            'ACCENT_5': '#9B30FF'
        }
        light_ocean_theme = {
            'ACCENT_1': '#2f4550',
            'ACCENT_2': '#2f4550',
            'ACCENT_3': '#586f7c',
            'ACCENT_4': '#000000',
            'ACCENT_5': '#9B30FF'
        }
        coffee_theme = {
            'ACCENT_1': '#997d60',
            'ACCENT_2': '#bbbcbf',
            'ACCENT_3': '#bca58d',
            'ACCENT_4': '#e3d1df',
            'ACCENT_5': '#9B30FF'
        }
        pastel_theme = {
            'ACCENT_1': '#EBC4AB',
            'ACCENT_2': '#C7EBC3',
            'ACCENT_3': '#9CB898',
            'ACCENT_4': '#E3D1DF',
            'ACCENT_5': '#B1ABEB'
        }

        def load_light_theme():
            create_file_with_theme(light_theme_default)

        def load_dark_theme():
            create_file_with_theme(dictionary_default_accents)

        def load_green_theme():
            create_file_with_theme(green_theme)

        def load_light_ocean_theme():
            create_file_with_theme(light_ocean_theme)

        def load_coffee_theme():
            create_file_with_theme(coffee_theme)

        def load_strawberry_theme():
            create_file_with_theme(strawberry_theme)

        def load_pastel_theme():
            create_file_with_theme(pastel_theme)

        lines_themes = [
            "Light Theme",
            "Dark Theme",
            "Strawberry Theme",
            "Green Theme",
            "Ocean Theme (Light)",
            "Coffee Theme",
            "Pastel Theme"
        ]

        dict_themes = {
            "1": load_light_theme,
            "2": load_dark_theme,
            "3": load_strawberry_theme,
            "4": load_green_theme,
            "5": load_light_ocean_theme,
            "6": load_coffee_theme,
            "7": load_pastel_theme
        }

        # Прокрутка возможных действий
        print('\n')
        functions_obs.StylishLook().scrolling_and_numbering_content(lines_themes)

        user_change_theme = input(standard_location(themes_location))
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
