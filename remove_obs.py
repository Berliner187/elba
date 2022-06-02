# -*- coding: UTF-8 -*-
import os
from time import sleep

from functions_obs import ProgramFunctions

from main import *


__version__ = '0.10-02'


class Remove(object):
	""" Удаление выбранного ресурса или заметки """

	def __init__(self, generic_key, category):
		self.category_object = category
		self.generic_key = generic_key

	def remove_object(self):
		system_action('clear')
		ProgramFunctions(self.generic_key, 'resource').get_category_label()
		template_some_message(ACCENT_3, '--- Change by number ---')

		folder = ''
		if self.category_object == 'resource':
			folder = FOLDER_WITH_RESOURCES
		elif self.category_object == 'note':
			folder = FOLDER_WITH_NOTES

		user_change = int(input(standard_location(f'/REMOVE_{str(self.category_object).upper()}')))
		try:
			template_remove_folder(folder + os.listdir(folder)[user_change-1])
		except IndexError:
			pass
