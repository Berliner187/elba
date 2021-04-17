from csv import DictReader, DictWriter
from shutil import copyfile
import os

__version__ = '1.0.0'

yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"
fields_for_main_data = ['resource', 'login', 'password']


def delete_resource():
	print(blue + '\n -- Change by number resource -- \n' + mc)
	change_res_by_num = int(input(yellow + ' - Resource number: ' + mc))
	file_date_base = 'volare/main_data.dat'
	# Выгрузка старого
	with open(file_date_base, encoding='utf-8') as saved_resource:
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
	new_file_date_base = 'new_data.dat'
	with open(new_file_date_base, mode="a", encoding='utf-8') as new_data:
		writer = DictWriter(new_data, fieldnames=fields_for_main_data)
		writer.writeheader()
		for i in range(cnt - 2):
			writer.writerow({
				'resource': mas_res[i],
				'login': mas_log[i],
				'password': mas_pas[i]
			})
		new_data.close()
	copyfile(new_file_date_base, file_date_base)    # Старый записывается новым файлом
	os.system('rm ' + new_file_date_base)   # Удаление нового файла
