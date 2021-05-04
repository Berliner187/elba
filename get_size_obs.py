#!/usr/bin/env python3
import os


size_mod_cache = 0
cache = '.pyc'
file_type = '.py'    # Модули заканчиваются на *obs.py
any_file = os.listdir('.')  # Поиск в текущей папке
files = []    # Массив для установленных модулей
for file in any_file:   # Итерация модулей
    if file.endswith(file_type):
        files.append(file)

cache_modules = []
direct = os.listdir('__pycache__/')
for item in direct:
    if item.endswith(cache):
        cache_modules.append(item)

for i in range(len(cache_modules)):
    size_mod_cache += os.path.getsize('__pycache__/' + cache_modules[i])

print('\n')

size_program = 0
for i in range(len(files)):
    size = os.path.getsize(files[i])
    print(size * 8, 'b', ' ----- ', files[i])
    size_program += size

size_program -= os.path.getsize('get_size_all.py')

print('\n Максимальный объем выделенной памяти в ОЗУ для программы:',
      33684 / 2**10,
      'Килобайт')

def rounding(size):
  """ Округление в килобайты """
  return round((size / 2**10), 1)

size_program += size_mod_cache  # Вычисление всего веса
print('\n Файлы программы заняли', rounding(size_program - size_mod_cache), 'Килобайт')
print('\n Кэш модулей занял', rounding(size_mod_cache) , 'Килобайт')
print('\n Итого весь проект занимает', rounding(size_program), 'Килобайт в ПЗУ \n')
