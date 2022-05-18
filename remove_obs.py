# -*- coding: UTF-8 -*-
import os
from time import sleep

from main import *


__version__ = '0.9-00'


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
			template_remove_folder(folder_category + item)