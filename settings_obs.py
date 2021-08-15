from main import *
from show_dec_data_obs import show_decryption_data


__version__ = 'P8.6_M1.0'


def settings(generic_key):
    system_action('clear')
    write_log('Settings', 'Run')
    template_some_message(GREEN, ' --- Settings --- ')
    # �������� ���������
    lines_set = [
        f'{ACCENT_3}1. {ACCENT_1}Customize colors accent'
    ]
    for line in lines_set:
        print(line)

    change_in_settings = input('\n - Change setting by number: ')
    if change_in_settings == '1':
        system_action('clear')

        dic_colors = ''
        with open(FILE_SETTINGS_COLOR, 'r') as f:
            for i in f.readlines():
                dic_colors = i
        dic_colors = eval(dic_colors)

        # ����� ��������, ������� ��������
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
        # ��������� �� ������ ���������
        for select in dic_colors:
            cnt += 1
            # ������������ �����
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
    show_decryption_data(generic_key, 'resource')
    write_log('Settings', 'Run')
