#!/usr/bin/env python3
from time import sleep
from os import system

YELLOW, BLUE, PURPLE, GREEN, RED, CLEAR_COLOR = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[31m", "\033[0m"


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
    sleep(TIMER)


def position_total():
    clear()
    print("                                                           ")
    print("  _____                      ______                        ")
    print(" |            |             |      \            /\         ")
    print(" |            |             |       \          /  \        ")
    print(" |            |             |       /         /    \       ")
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)
    # print(CLEAR_COLOR)

def author():
    print(YELLOW)
    print("  ___                ___                                                                     ")
    print(" |   \              |   \                                                  ___   ____        ")  
    print(" |    \             |    \   __    __        o          __   __      /|   |   |      /       ")
    print(" |____/   \  /      |____/  |     |  \  |    |  |\   | |    |  \      |   |___|     /        ")
    print(" |    \    \/       |    \  |__   |__/  |    |  | \  | |__  |__/      |   |   |    /         ")
    print(" |     |   /        |     | |     |  \  |    |  |  \ | |    |  \      |   |   |   /          ")
    print(" |_____/  /         |_____/ |___  |   \ |___ |  |   \| |___ |   \     |   |___|  /           ")
    print('\n'*3)
    



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
        # position_7()
        # position_6()
        # position_5()
        # position_4()
        # position_3()
        # position_2()
        # position_1()
        # position_0()


def elba():     # Фунция вывода только логотипа
    print(PURPLE)
    print("  _____                      ______                        ")
    print(" |            |             |      \            /\         ")
    print(" |            |             |       \          /  \        ")
    print(" |            |             |       /         /    \       ")
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    print(CLEAR_COLOR)
