#!/usr/bin/env python3
from time import sleep
from os import system
from time import sleep
from random import choice

import shutil
import sys
import os

from main import *


__version__ = '1.3.1'


cols, rows = shutil.get_terminal_size()


def wait_effect(lines, sleeper):
    for line in lines:
        for c in line.center(cols):
            print(c, end='')
            sys.stdout.flush()
            sleep(sleeper)
        print('')


logo_strings_row = [
        "",
        " EEEEEEEE     LL            BBBBBBB            AAAA         ",
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
    YELLOW,
    " ___              ___                                                                 ",
    "|   \            |   \                                                  ___   ____    ",
    "|    \           |    \   __    __        o          __   __      /|   |   |      /   ",
    "|____/   \  /    |____/  |     |  \  |    |  |\   | |    |  \      |   |___|     /    ",
    "|    \    \/     |    \  |__   |__/  |    |  | \  | |__  |__/      |   |   |    /     ",
    "|     |   /      |     | |     |  \  |    |  |  \ | |    |  \      |   |   |   /      ",
    "|_____/  /       |_____/ |___  |   \ |___ |  |   \| |___ |   \     |   |___|  /       ",
    BLUE, "________________________________________________________________________________"
]


def logo():
    # <<< Построчная отрисовка лого >>>
    wait_effect(logo_strings_row, 0.000003)


def author():
    print(YELLOW)
    for i in author_emb:
        print(i.center(cols))
        sleep(.1)


def animation():
    cols, rows = shutil.get_terminal_size()
    while True:
        system_action('clear')
        print(PURPLE)
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
                print(BLUE)
            else:
                print(YELLOW)
            wait_effect(logo_strings_row, 0.000001)
            sleep(.1)


def elba():
    logo()


def Ukraine():
    print(BLUE, "  __________________________________________________________")
    print(BLUE, " /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ")
    print(BLUE, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(BLUE, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(BLUE, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(BLUE, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(BLUE, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(BLUE, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(BLUE, " ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ ")
    print(YELLOW, " /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ")
    print(YELLOW, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(YELLOW, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(YELLOW, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(YELLOW, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(YELLOW, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(YELLOW, "|/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\|")
    print(YELLOW, " -------------------------------------------------------------")
    sleep(2)


def first_start_message():
    global cols
    lines = [
        BLUE,
        ("\n  - Encrypt your passwords with one master-password -    ".center(cols)),
        ("\n  -           No resources saved. Add them!         -  \n".center(cols)),
        ("\n ----                That's easy!                 ---- \n".center(cols)),
        RED,
        ("\n          Программа не поддерживает русский язык         ".center(cols)),
    ]
    wait_effect(lines, 0.001)
