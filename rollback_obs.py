# -*- coding: UTF-8 -*-
from main import *

import os
from time import sleep


__version__ = '0.10-01'


def rollback():
    """ Откат к сохраненным версиям """
    s = 0
    system_action('clear')
    for version in os.listdir(OLD_ELBA):
        s += 1
        print(f"{s} - {ACCENT_1}{version}{ACCENT_4}")

    template_some_message(ACCENT_3, "  - Change version by number - ")
    change = int(input(ACCENT_1 + f"(1-{s}): " + ACCENT_4))
    if change == '-z':
        template_remove_folder(OLD_ELBA)
    cnt = 0
    for need_version_folder in os.listdir(OLD_ELBA):
        cnt += 1
        if cnt == change:
            for item in os.listdir(OLD_ELBA + need_version_folder):
                if item.endswith('.py'):
                    os.system(get_peculiarities_system('copy_file') + OLD_ELBA + need_version_folder + '/' + item + ' .')
            template_remove_folder(FOLDER_WITH_DATA)
            os.system(
                get_peculiarities_system('copy_dir') + OLD_ELBA + need_version_folder + '/' + FOLDER_WITH_DATA + '/' + ' .'
            )
    system_action('clear')
    template_some_message(GREEN, '  --- Success roll back! --- ')
    write_log('Roll back', 'Done')
    sleep(1)
