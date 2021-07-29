#!/usr/bin/env python3
from time import sleep
from os import system
from time import sleep

import shutil
import sys
import os

from main import *


__version__ = '1.2.1'


def clear():
    system('clear')


TIMER = .08
STRING_LINE = "___________________________________________________________ \n"
STRING_BOTTOM_0 = " |__________  |__________   |_________/  /              \  "
STRING_BOTTOM_1 = " |            |             |         |   /            \   "


def template(string, cnt_str):
    clear()
    print(STRING_LINE * cnt_str)
    print(string)
    sleep(TIMER)


def position_0():
    print(PURPLE)
    template(STRING_LINE, 9)


def position_1():
    clear()
    print(STRING_LINE * 8)
    print(STRING_BOTTOM_1)
    sleep(TIMER)


def position_2():
    clear()
    print(STRING_LINE * 7)
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_3():
    clear()
    print(STRING_LINE * 6)
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_4():
    clear()
    print(STRING_LINE * 5)
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_5():
    clear()
    print(STRING_LINE * 4)
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_6():
    clear()
    print(STRING_LINE * 3)
    print(" |            |             |       /         /    \       ")
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_7():
    clear()
    print(STRING_LINE * 2)
    print(" |            |             |       \          /  \        ")
    print(" |            |             |       /         /    \       ")
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_8():
    clear()
    print(STRING_LINE)
    print(" |            |             |      \            /\         ")
    print(" |            |             |       \          /  \        ")
    print(" |            |             |       /         /    \       ")
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    author()
    sleep(TIMER)


def wait_effect(lines, sleeper):
    for line in lines:  # for each line of text (or each message)
        for c in line:  # for each character in each line
            print(c, end='')  # print a single character, and keep the cursor there.
            sys.stdout.flush()  # flush the buffer
            sleep(sleeper)  # wait a little to make the effect look good.
        print('')


def logo():
    cols, rows = shutil.get_terminal_size()
    # print(YELLOW)
    # lines = [
    #     ("WELLCOME TO:        ").center(cols)
    # ]
    # wait_effect(lines, 0.0002)
    print(BLUE)
    logo_lines = [
        ("                                                            ").center(cols),
        ("  EEEEEEE     LL            BBBBBBB            AAAA         ").center(cols),
        (" E            LL            B      B         A      A       ").center(cols),
        (" E            LL            B      BB       AA      AA      ").center(cols),
        (" EEEEEEE      LL            BBBBBBBB       AAAAAAAAAAAA     ").center(cols),
        (" E            LL            B      BB      AA        AA     ").center(cols),
        (" E            LL            B       BB     AA        AA     ").center(cols),
        (" E            LL            B        BB    AA        AA     ").center(cols),
        (" E            LL            B         BB   AA        AA     ").center(cols),
        (" EEEEEEEEEEE  LLLLLLLLLLL   BBBBBBBBBBB    AA        AA     ").center(cols)
    ]
    wait_effect(logo_lines, 0.00001)


def position_total():
    clear()
    logo()
    sleep(TIMER)


def author():
    print(YELLOW)
    print("  ___                ___                                                                     ")
    print(" |   \              |   \                                                  ___   ____        ")
    print(" |    \             |    \   __    __        o          __   __      /|   |   |      /       ")
    print(" |____/   \  /      |____/  |     |  \  |    |  |\   | |    |  \      |   |___|     /        ")
    print(" |    \    \/       |    \  |__   |__/  |    |  | \  | |__  |__/      |   |   |    /         ")
    print(" |     |   /        |     | |     |  \  |    |  |  \ | |    |  \      |   |   |   /          ")
    print(" |_____/  /         |_____/ |___  |   \ |___ |  |   \| |___ |   \     |   |___|  /           ")
    print(BLUE, "__________________________________________________________________________________________________")


def animation():
    while True:
        position_0()
        position_1()
        position_2()
        position_3()
        position_4()
        position_5()
        position_6()
        position_7()
        position_8()
        position_total()
        author()
        sleep(2)
        position_7()
        position_6()
        position_5()
        position_4()
        position_3()
        position_2()
        position_1()
        position_0()


def elba():     # Фунция вывода только логотипа
    logo()
    print(DEFAULT_COLOR)


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


# lines = [BLUE,
#         " || Delta For Linux  || ",
#         " || by Berliner187   || ",
#         " || Veli Afaline     || ", YELLOW, __version__
#     ]
# wait_effect(lines)
# first_start_message()
# elba()
