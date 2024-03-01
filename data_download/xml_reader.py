from decimal import Decimal
import csv
import xml.etree.ElementTree as ET
import os
import sys
import django
sys.path.extend(['/home/SC/lisenko/Project/demographics', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demographics.settings")
django.setup()
from demographics_monitor.models import DemographicStatistics, Indicators, Territories


# Загрузка XML данных
root = ET.parse('tbl_values.xml').getroot()
id_indicator = 422
indicator = Indicators.objects.get(pk=id_indicator)
list_id_territory = list(range(2, 73))
list_id_territory.append(182)

for id_territory in list_id_territory:
    # Получение объекта Territories по их ID
    territory = Territories.objects.get(pk=id_territory)
    indicator_values = []
    for value in root.findall('.//tbl_values'):
        code_indicator = value.find('code_indicator')
        district = value.find('district')
        population = value.find('population')
        if code_indicator is not None and district is not None:
            if code_indicator.text == '173' and district.text == str(id_territory):
                value_indicator = Decimal(value.find('value_indicator').text)
                period = int(value.find('period').text)
                indicator_values.append((value_indicator, period))

    sorted_indicator_values = sorted(indicator_values, key=lambda x: x[1])
    for element in sorted_indicator_values:
        print(element)

    print(f'Будет добавлено {len(sorted_indicator_values)} записей!')
    append_data = input(f'Добавить данные показателя "{indicator.indicator_name}" в {territory.territory_name}? y/n ')
    if append_data == 'y':
        for element in sorted_indicator_values:
            # Создание объекта модели и сохранение его в базу данных
            DemographicStatistics.objects.create(
                indicator=indicator,
                territory=territory,
                value=element[0],
                year=element[1],
                is_approved=True,
            )
        print('Данные добавлены!')

"""
# Загрузка XML данных
root = ET.parse('tbl_values.xml').getroot()
id_indicator = 416
id_territory = 51

# Получение объектов Indicators и Territories по их ID
indicator = Indicators.objects.get(pk=id_indicator)
territory = Territories.objects.get(pk=id_territory)
indicator_values = []
for value in root.findall('.//tbl_values'):
    code_indicator = value.find('code_indicator')
    district = value.find('district')
    population = value.find('population')    
    if code_indicator is not None and district is not None and population is not None:
        # if code_indicator.text == '171' and district.text == '1' and population.text == '1':
        if code_indicator.text == '171' and district.text == str(id_territory):
            value_indicator = Decimal(value.find('value_indicator').text)
            period = int(value.find('period').text)
            # print(f'{(value_indicator, period)}')
            indicator_values.append((value_indicator, period))

sorted_indicator_values = sorted(indicator_values, key=lambda x: x[1])
for element in sorted_indicator_values:
    print(element)

print(f'Будет добавлено {len(sorted_indicator_values)} записей!')
append_data = input(f'Добавить данные показателя "{indicator.indicator_name}" в {territory.territory_name}? y/n ')
if append_data == 'y':
    for element in sorted_indicator_values:
        # Создание объекта модели и сохранение его в базу данных
        DemographicStatistics.objects.create(
            indicator=indicator,
            territory=territory,
            value=element[0],
            year=element[1],
            is_approved=True,
        )
    print('Данные добавлены!')
"""

# ВЕДУ РАСЧЕТ ИНДЕКСА И ДОБАВЛЯЮ ЗНАЧЕНИЕ В БД
""" 
conn = sqlite3.connect('../db.sqlite3')  # установка соединения.
cur = conn.cursor()  # создание курсора
sql = "SELECT value, year FROM demographics_monitor_demographicstatistics WHERE indicator_id = 415"  # выполнение запроса
cur.execute(sql)
rows413 = cur.fetchall() # получение всех строк результата
conn.close() # закрытие соединения

conn = sqlite3.connect('../db.sqlite3')  # установка соединения.
cur = conn.cursor()  # создание курсора
sql = "SELECT value, year FROM demographics_monitor_demographicstatistics WHERE indicator_id = 412"  # выполнение запроса
cur.execute(sql)
rows410 = cur.fetchall() # получение всех строк результата
conn.close() # закрытие соединения

rows = []
id_indicator = 424
for y in range(1990, 2023):
    for row413 in rows413:
        for row410 in rows410:
            if row413[1] == y and row410[1] == y:
                value_indicator = round(row413[0]/row410[0]*100, 2)
                print(f'{y} - {row413[0]} - {row410[0]} = {value_indicator}') # вывод значений столбца "value"                
                period = y
                rows.append((value_indicator, period, True, datetime.datetime.now(), datetime.datetime.now(), id_indicator, 1))
print(f'Будет добавлено {len(rows)} записей!')
indicator = input('Добавить данные? y/n ')
if indicator == 'y':
    # Загрузим данные в новую БД
    conn = sqlite3.connect('../db.sqlite3')  # установка соединения
    cur = conn.cursor()  # создаем курсор
    # Создаем SQL команду для добавления данных
    sql = '''INSERT INTO demographics_monitor_demographicstatistics(value, year, is_approved, time_create, time_update, indicator_id, territory_id) VALUES(?, ?, ?, ?, ?, ?, ?)'''
    cur.executemany(sql, rows)
    conn.commit()
    cur.execute("PRAGMA optimize")
    cur.execute("PRAGMA vacuum")
    conn.close()
    print(f'Данные добавлены!')
 """