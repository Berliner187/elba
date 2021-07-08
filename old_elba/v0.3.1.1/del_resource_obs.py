from csv import DictReader, DictWriter
from shutil import copyfile
import os

from time import sleep

from main import *


__version__ = '2.0.1'  # Версия модуля


def delete_resource(category):
	print(BLUE + '\n -- Change by number -- \n' + DEFAULT_COLOR)

	folder_category = ''
	if category == 'resource':
		folder_category = FOLDER_WITH_RESOURCES
	elif category == 'note':
		folder_category = FOLDER_WITH_NOTES

	change_res_by_num = int(input(YELLOW + ' - Change number: ' + DEFAULT_COLOR))
	s = 0
	for item in os.listdir(folder_category):
		s += 1
		if s == change_res_by_num:
			os.system("rm -r " + folder_category + item)
