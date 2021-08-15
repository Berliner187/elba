# -*- coding: UTF-8 -*-
from csv import DictReader, DictWriter
from shutil import copyfile
import os
from time import sleep

from main import *


__version__ = 'P8.6_M1.0'


def delete_object(category):
	""" Удаление выбранного ресурса или заметки """
	template_some_message(ACCENT_3, ' -- Change by number -- ')

	folder_category = ''
	if category == 'resource':
		folder_category = FOLDER_WITH_RESOURCES
	elif category == 'note':
		folder_category = FOLDER_WITH_NOTES

	change_res_by_num = int(input(f"{ACCENT_1} - Change number: {ACCENT_4}"))
	s = 0
	for item in os.listdir(folder_category):
		s += 1
		if s == change_res_by_num:
			os.system(get_peculiarities_system("rm_dir") + folder_category + item)
