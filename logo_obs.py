#!/usr/bin/env python3
from time import sleep
from os import system
from time import sleep
from random import choice

import shutil
import sys
import os

from main import *


__version__ = 'P8.6_M1.0'


cols = get_size_of_terminal()


def wait_effect(lines, sleeper):
    crutch = sleeper
    for line in lines:
        for c in line.center(cols):
            if c == ' ':
                sleeper = 0
            else:
                sleeper = crutch
            print(c, end='')
            sys.stdout.flush()
            sleep(sleeper)
        print('')


logo_strings_row = [
        "",
        " EEEEEEEE     LL            BBBBBBB           AAAAAA        ",
        " E            LL            B      B         A      A       ",
        " E            LL            B      BB       AA      AA      ",
        " EEEEEEE      LL            BBBBBBBB       AAAAAAAAAAAA     ",
        " E            LL            B      BB      AA        AA     ",
        " E            LL            B       BB     AA        AA     ",
        " E            LL            B        BB    AA        AA     ",
        " E            LL            B         BB   AA        AA     ",
        " EEEEEEEEEEE  LLLLLLLLLLL   BBBBBBBBBBB    AA        AA     "
    ]


author_emb = [
    ACCENT_1,
    " ___              ___                                                                 ",
    "|   \            |   \                                                  ___   ____    ",
    "|    \           |    \   __    __        o          __   __      /|   |   |      /   ",
    "|____/   \  /    |____/  |     |  \  |    |  |\   | |    |  \      |   |___|     /    ",
    "|    \    \/     |    \  |__   |__/  |    |  | \  | |__  |__/      |   |   |    /     ",
    "|     |   /      |     | |     |  \  |    |  |  \ | |    |  \      |   |   |   /      ",
    "|_____/  /       |_____/ |___  |   \ |___ |  |   \| |___ |   \     |   |___|  /       ",
    ACCENT_3, "________________________________________________________________________________"
]


def logo():
    # <<< Посимвольная отрисовка лого >>>
    wait_effect(logo_strings_row, 0.00003)


def author():
    print(ACCENT_1)
    for i in author_emb:
        print(i.center(cols))
        sleep(.1)


def animation():
    while True:
        system_action('clear')
        print(ACCENT_2)
        for row in logo_strings_row:
            print(row.center(cols))
            sleep(0.09)
        author()
        sleep(1)
        cnt = 0
        system_action('clear')
        for i in range(10):
            system_action('clear')
            cnt += 1
            if cnt % 2 == 0:
                print(ACCENT_3)
            else:
                print(ACCENT_1)
            wait_effect(logo_strings_row, 0.00001)
            sleep(.1)


def elba():
    print(ACCENT_1)
    logo()


def Ukraine():
    system_action('clear')
    lines_flag = [
        ACCENT_3,
        "  __________________________________________________________  ",
        " /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        f"      ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ {ACCENT_1}",
        "  __________________________________________________________  ",
        " /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|",
        " -------------------------------------------------------------"
    ]
    wait_effect(lines_flag, .0006)
    sleep(2)
    system_action('clear')
    logo()
    sleep(2)
    animation()


def first_start_message():
    lines = [
        ACCENT_3,
        "  - Encrypt your passwords with one master-password -  ",
        "  -           No resources saved. Add them!         -  ",
        " ----                That's easy!                 ---- ",
        RED,
        "          Программа не поддерживает русский язык       ",
        ACCENT_4
    ]
    wait_effect(lines, 0.03)
