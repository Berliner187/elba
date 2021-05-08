from csv import DictReader, DictWriter
from shutil import copyfile
import os

from time import sleep

from main import *


__version__ = '2.0.1'  # Версия модуля


def delete_resource():
	print(BLUE + '\n -- Change by number -- \n' + DEFAULT_COLOR)
	change_res_by_num = int(input(YELLOW + ' - Resource number: ' + DEFAULT_COLOR))
	s = 0
	for item in os.listdir(FOLDER_WITH_RESOURCES):
		s += 1
		if s == change_res_by_num:
			os.system("rm -r " + FOLDER_WITH_RESOURCES + item)
