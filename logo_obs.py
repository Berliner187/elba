#!/usr/bin/env python3
from time import sleep
from os import system

YELLOW, BLUE, PURPLE, GREEN, RED, CLEAR_COLOR = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[31m", "\033[0m"


def clear():
    system('clear')


# def template(string, cnt_str):
#     clear()
#     print("___________________________________________________________ \n" * cnt_str)
#     print(string)
#     cnt_str -= 1
#     sleep(.25)

TIMER = .13


def position_0():
    clear()
    print(PURPLE)
    print("___________________________________________________________ \n" * 9)
    sleep(TIMER)


def position_1():
    clear()
    print("___________________________________________________________ \n" * 8)
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)



def position_2():
    clear()
    print("___________________________________________________________ \n" * 7)
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)



def position_3():
    clear()
    print("___________________________________________________________ \n" * 6)
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_4():
    clear()
    print("___________________________________________________________ \n" * 5)
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)



def position_5():
    clear()
    print("___________________________________________________________ \n" * 4)
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_6():
    clear()
    print("___________________________________________________________ \n" * 3)
    print(" |            |             |       /         /    \       ")
    print(" |------      |             |______/         /______\      ")
    print(" |            |             |       \       /        \     ")
    print(" |            |             |        \     /          \    ")
    print(" |            |             |         |   /            \   ")
    print(" |__________  |__________   |_________/  /              \  ")
    sleep(TIMER)


def position_7():
    clear()
    print("___________________________________________________________ \n" * 2)
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
    print("___________________________________________________________ \n")
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
        position_7()
        position_6()
        position_5()
        position_4()
        position_3()
        position_2()
        position_1()
        position_0()


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
