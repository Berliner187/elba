from csv import DictReader, DictWriter
from shutil import copyfile
import os
# Импорт главной папки и файла с данными
from main import *


__version__ = '2.0.0 ON DEVELOPMENT STAGE'  # Версия модуля


def delete_resource():
	print(BLUE + '\n -- Change by number -- \n' + DEFAULT_COLOR)
	change_res_by_num = int(input(YELLOW + ' - Resource number: ' + DEFAULT_COLOR))
	# Выгрузка старого
	with open(FILE_FOR_RESOURCE, encoding='utf-8') as saved_resource:
		reader = DictReader(saved_resource, delimiter=',')
		mas_res, mas_log, mas_pas = [], [], []
		cnt = 0
		for row in reader:
			cnt += 1
			if cnt == change_res_by_num:    # Перескакивает выбранный юзером и не добавляется
				cnt += 1
			else:   # Нужные ресурсы добавляются в массивы
				mas_res.append(row["resource"])
				mas_log.append(row["login"])
				mas_pas.append(row["password"])
		saved_resource.close()
	# Перенос в новый файл
	NEW_FILE_FOR_RESOURCE = 'new_data.dat'
	with open(NEW_FILE_FOR_RESOURCE, mode="a", encoding='utf-8') as new_data:
		writer = DictWriter(new_data, fieldnames=fields_for_main_data)
		writer.writeheader()
		for i in range(cnt - 2):
			writer.writerow({
				fields_for_main_data[0]: mas_res[i],
				fields_for_main_data[1]: mas_log[i],
				fields_for_main_data[2]: mas_pas[i]
			})
		new_data.close()
	copyfile(NEW_FILE_FOR_RESOURCE, FILE_FOR_RESOURCE)    # Старый записывается новым файлом
	os.system('rm ' + NEW_FILE_FOR_RESOURCE)   # Удаление нового файла
