#!/usr/bin/env python3
from time import sleep
from os import system
from time import sleep
from random import choice

import shutil
import sys
import os

from main import *


__version__ = '0.10-02'


cols = get_size_of_terminal()


def iterate_over_characters(string, sleeper):
    """ Анимация печати символов """
    crutch = sleeper
    for c in string.center(cols):
        if c == ' ':
            sleeper = 0
        else:
            sleeper = crutch
        print(c, end='')
        sys.stdout.flush()
        sleep(sleeper)
    print('')


def wait_effect(lines, sleeper):
    for line in lines:
        iterate_over_characters(line, sleeper)


logo_strings_row = [
    ACCENT_5,
    "EEEEEEEEEEEEEE    LL                 BBBBBBBBBB           AAAAAAAAAAAAA ",
    "                  LL                          BB         AA           AA",
    "                  LL                           BB                       ",
    "                  LL                          BB                        ",
    "EEEEEEEEEEEEEE    LL                 BBBBBBBBBB          AAAAAAAAAAAAAAA",
    "                  LL                 BB       BB         AA           AA",
    "                  LL                 BB        BB        AA           AA",
    "                  LL                 BB          BB      AA           AA",
    "                  LL                 BB           BB     AA           AA",
    "                  LL                 BB          BB      AA           AA",
    "EEEEEEEEEEEEEE    LLLLLLLLLLLLLLL    BBBBBBBBBBBB        AA           AA",
    ACCENT_4,
]


hello = [
        "",
        "HH        HH   EEEEEEEE      LL            LL             OOOOOOOOO ",
        "HH        HH   EE            LL            LL            OO       OO",
        "HH        HH   EE            LL            LL            OO       OO",
        "HHHHHHHHHHHH   EEEEEEE       LL            LL            OO       OO",
        "HH        HH   EE            LL            LL            OO       OO",
        "HH        HH   EE            LL            LL            OO       OO",
        "HH        HH   EE            LL            LL            OO       OO",
        "HH        HH   EE            LL            LL            OO       OO",
        "HH        HH   EEEEEEEEEEE   LLLLLLLLLLL   LLLLLLLLLLL    OOOOOOOOO "
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
    ACCENT_3, "________________________________________________________________________________",
    ACCENT_5,
    "            ;ol:;;;;:::;,'.                                                          ...         ..                                   ",
    "         ,OWWWWWKooONNKx:.                             ..                     .lkKK:      .:x0x.                               .:ox;",
    "         .dMMMMMO. 'kWMMWO,                          'oO;                     ,KMMN:      ;KMM0'                               :NMWo",
    "         .dMMMMMk.  :XMMMMK;     ,:.    ,c, .;ll:',oOXWWd.  .:l:.       .c,   ;KMMX:..,.  ;XMM0'    'cl;.    'c:.  .::.      'ckWMWo",
    "         .dMMMMMk.  'OMMMMMk.  'xNW0: .oXMX:,0MMNc.:0MMWo..lOXWWO,   .oOKWNkl.;KMMNOkXWO' ;XMM0'.:cl0WMNO, .lXMWOlxXWWo    .oKWMMMWo",
    "         .dMMMMMk.  .kMMMMMK;.oxlkWMXl.oWMWo;0MMNc .xMMNc.xWN0xd:.  'kxccll:. ;KMMNxxNMWO';XMM0' ...,kWMWd. lNMMKcdWMMx.  :0d;xNMMWo",
    "         .dMMMMMk.  .kMMMMMKcdNd.'OW0: cNMWo;0MMNc .xMMNc.xWMW0c.  .xXc       ,KMMX:.xWMWocXMM0'  'ld0WMMx. lNMM0,:NMMx. cXK; .xMMWo",
    "          dMMMMMO.  .kMMMMMOoKM0oxkc.  cNMWo;0MMNc .xMMNc .oXMMWO; ,KWk;.     ,KMMN: ;XMMklKMM0'.lXKcdWMMx. lNMM0,:NMMx..OMX; .dWMWo",
    "         .dMMMMMk.  ,0MMMMXc;KMMNd.    cNMWo;0MMNc .xMMNc   'dXMMNocKMWXx.    ,KMMN: .OMWdlKMMO,lNMx.cNMMx. lNMM0,:NMMx.,KMWk..dWMWo",
    "         .dMMMMMk. .oNMMMXl .oNMW0c.   cNMWo;0MMNc .xMMNc  .,;ckNMO;dWMMW0:.  ,KMMN: .kMX::XMM0;dMM0,:XMMx. lNMM0,:NMMx..kWMWOlkWMWo",
    "         .xMMMMM0c:xNMWXx,   .lXMMW0;  cNMM0xKMMWo .xMMWd'c0NNK0KO; .oXMMMWk. ,KMMX: '0No.;XMMO,cXMW0ONMMk. lNMM0,:XMM0' 'OWMMNKWMWx.",
    "         'oocclodxkkkdc'       'oOkc.  .dOxc,ckOd,  ;kOd,..,ckOd,.    'cd0x,  'x00k, lKo. ,kKKx..cOkc;dK0c. ;O00x..dKOc.  .lOk:'lOk:."
]


def logo():
    # <<< Посимвольная отрисовка лого >>>
    for line in logo_strings_row:
        print(line.center(cols))


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
        sleep(3)
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


def first_start_message():
    """ Сообщения в самом начале """
    def template_elba_say():
        elba_say_list = [
            'Your data is kept confidential through Elba.',
            'Only you know your service passwords.',
            'Your notes will remain secret.',
            'The files will be hidden under lock and key.',
            RED + 'Нет поддержки русского языка.'
        ]
        for string in elba_say_list:
            sleep(1)
            iterate_over_characters(standard_location('/SAY') + ACCENT_3 + string, 0.03)
            sleep(1)

    sleep(1)
    system_action('clear')
    print(ACCENT_4)
    wait_effect(hello, 0.02)    # Приветствие
    sleep(3)
    system_action('clear')
    print(ACCENT_5)
    wait_effect(logo_strings_row, 0.02)
    print(ACCENT_3)
    template_elba_say()
    input(ACCENT_4 + '\n Proceed...')
    system_action('clear')
