from csv import DictReader, DictWriter
from shutil import copyfile
import os
# Импорт главной папки и файла с данными
from main import main_folder, fields_for_main_data
# Импорт цветов
from main import yellow, blue, purple, green, mc, red


__version__ = '1.0.2'	# Версия модуля


def delete_resource():
	print(blue + '\n -- Change by number -- \n' + mc)
	change_res_by_num = int(input(yellow + ' - Resource number: ' + mc))
	file_date_base = main_folder + 'main_data.dat'
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
				fields_for_main_data[0]: mas_res[i],
				fields_for_main_data[1]: mas_log[i],
				fields_for_main_data[2]: mas_pas[i]
			})
		new_data.close()
	copyfile(new_file_date_base, file_date_base)    # Старый записывается новым файлом
	os.system('rm ' + new_file_date_base)   # Удаление нового файла
