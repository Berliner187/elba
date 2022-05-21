# -*- coding: UTF-8 -*-
from main import *

import os
import functions_obs
from time import sleep


__version__ = '0.10-02'


def rollback():
    """ Откат к сохраненным версиям """
    system_action('clear')
    functions_obs.StylishLook().topper('ROLLBACK')
    cnt_versions = functions_obs.StylishLook().scrolling_and_numbering_content(os.listdir(OLD_ELBA))

    template_some_message(ACCENT_3, "  - Change version by number - ")
    change = int(input(ACCENT_1 + f"(1-{cnt_versions}): " + ACCENT_4))
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
