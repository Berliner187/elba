#!/usr/bin/env python3
from time import sleep
from os import system
from time import sleep
from random import choice

import shutil
import sys
import os

from main import *


__version__ = '1.3.0'


def wait_effect(lines, sleeper):
    cols, rows = shutil.get_terminal_size()
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


def logo():
    # <<< Построчная отрисовка лого >>>
    wait_effect(logo_strings_row, 0.000003)


def author():
    print(YELLOW)
    print("  ___                ___                                                                 ")
    print(" |   \              |   \                                                  ___   ____    ")
    print(" |    \             |    \   __    __        o          __   __      /|   |   |      /   ")
    print(" |____/   \  /      |____/  |     |  \  |    |  |\   | |    |  \      |   |___|     /    ")
    print(" |    \    \/       |    \  |__   |__/  |    |  | \  | |__  |__/      |   |   |    /     ")
    print(" |     |   /        |     | |     |  \  |    |  |  \ | |    |  \      |   |   |   /      ")
    print(" |_____/  /         |_____/ |___  |   \ |___ |  |   \| |___ |   \     |   |___|  /       ")
    print(BLUE, "___________________________________________________________________________________")


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
    cols, rows = shutil.get_terminal_size()
    lines = [
        BLUE,
        ("\n  - Encrypt your passwords with one master-password -    ".center(cols)),
        ("\n  -           No resources saved. Add them!         -  \n".center(cols)),
        ("\n ----                That's easy!                 ---- \n".center(cols)),
        RED,
        ("\n          Программа не поддерживает русский язык         ".center(cols)),
        YELLOW,
        ("\n --              Pick a master-password               -- ".center(cols))
    ]
    wait_effect(lines, 0.001)
