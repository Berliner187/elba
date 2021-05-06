from main import *
from main import __version__
import datetime


def write_log(cause, status):   # Функция записи в файл версии

    def get_date():      # Получение и форматирование текущего времени
        hms = datetime.datetime.today()  # Дата и время
        day, month, year = hms.day, hms.month, hms.year     # Число, месяц, год
        hour = hms.hour  # Формат часов
        minute = hms.minute  # Формат минут
        second = hms.second  # Формат секунд
        time_format = str(hour) + ':' + str(minute) + ':' + str(second)
        date_format = str(day) + '.' + str(month) + '.' + str(year)
        total = str(time_format) + '-' + str(date_format)
        return ''.join(total)

    with open(FILE_LOG, mode="a", encoding='utf-8') as log_data:
        log_writer = DictWriter(log_data, fieldnames=fields_for_log, delimiter=';')

        log_writer.writerow({
            fields_for_log[0]: __version__,     # Запись версии
            fields_for_log[1]: get_date(),     # Запись даты и времени
            fields_for_log[2]: cause,     # Запись причины
            fields_for_log[3]: status})  # Запись статуса
