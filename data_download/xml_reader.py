from decimal import Decimal
import csv
import xml.etree.ElementTree as ET
import os
import sys
import django
import sqlite3
from datetime import datetime
sys.path.extend(['/home/SC/lisenko/Project/demographics', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demographics.settings")
django.setup()
from demographics_monitor.models import DemographicStatistics, Indicators, Territories


# Загрузка XML данных по одной территории (по АК)

root = ET.parse('tbl_values.xml').getroot()
id_indicator = 371
id_territory = 1
indicator = Indicators.objects.get(pk=id_indicator)
territory = Territories.objects.get(pk=id_territory)
indicator_values = []
for value in root.findall('.//tbl_values'):
    code_indicator = value.find('code_indicator')
    district = value.find('district')
    gender = value.find('gender')
    age_category = value.find('age_category')
    population = value.find('population')

    # if code_indicator.text == '124' and district.text == '1' and gender.text == '1' and age_category.text == '2' and population.text == '1':
    if code_indicator is not None and district is not None and population is not None:
        if code_indicator.text == '144' and district.text == '1' and gender.text == '3' and age_category.text == '4' and population.text == '3':
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
        DemographicStatistics.objects.create(
            indicator=indicator,
            territory=territory,
            value=element[0],
            year=element[1],
            is_approved=True,
        )

    print('Данные добавлены!')


# Загрузка XML данных МО
"""
root = ET.parse('tbl_values.xml').getroot()
id_indicator = 303
indicator = Indicators.objects.get(pk=id_indicator)
# list_id_territory = list(range(157, 181)) + list(range(183, 226))
list_id_territory = list(range(2, 73)) + [182]

for id_territory in list_id_territory:
    # Получение объекта Territories по их ID
    territory = Territories.objects.get(pk=id_territory)
    indicator_values = []
    for value in root.findall('.//tbl_values'):
        code_indicator = value.find('code_indicator')
        district = value.find('district')
        gender = value.find('gender')
        age_category = value.find('age_category')
        population = value.find('population')
        if code_indicator is not None and district is not None:
            if code_indicator.text == '143' and district.text == str(id_territory) and gender.text == '1':
                value_indicator = Decimal(value.find('value_indicator').text)
                period = int(value.find('period').text)
                indicator_values.append((value_indicator, period))
    sorted_indicator_values = sorted(indicator_values, key=lambda x: x[1])
    for element in sorted_indicator_values:
        print(element)
    for element in sorted_indicator_values:
        # Создание объекта модели и сохранение его в базу данных
        DemographicStatistics.objects.create(
            indicator=indicator,
            territory=territory,
            value=element[0],
            year=element[1],
            is_approved=True,
        )
    print(f'Данные показателя "{indicator.indicator_name}" в {territory.territory_name} добавлены в кол-ве {len(sorted_indicator_values)} записей!')
"""

# Расчет и добавление значений в БД
# Темп прироста
"""
conn = sqlite3.connect('../db.sqlite3')  # установка соединения.
cur = conn.cursor()  # создание курсора
sql = "SELECT value, year FROM demographics_monitor_demographicstatistics WHERE indicator_id = 66"  # выполнение запроса
cur.execute(sql)
rows192 = cur.fetchall()  # получение всех строк результата
conn.close()  # закрытие соединения

# Вычисление темпа прироста
growth_rates = []
for i in range(1, len(rows192)):
    current_value = rows192[i][0]
    previous_value = rows192[i-1][0]
    growth_rate = (current_value - previous_value) / previous_value
    growth_rates.append(growth_rate)

rows = []
id_indicator = 197
for year, growth_rate in zip([row[1] for row in rows192[1:]], growth_rates):
    value_indicator = round(growth_rate * 100, 2)
    rows.append((value_indicator, year, True, datetime.now(), datetime.now(), id_indicator, 1))

for row in rows:
    print(row)
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

"""
# Темп прироста для МО
list_id_territory = list(range(2, 73)) + [182]
for id_territory in list_id_territory:
    conn = sqlite3.connect('../db.sqlite3')  # установка соединения.
    cur = conn.cursor()  # создание курсора
    sql = "SELECT value, year FROM demographics_monitor_demographicstatistics WHERE indicator_id = 192 AND territory_id = ?"  # выполнение запроса
    cur.execute(sql, (id_territory,))
    rows192 = cur.fetchall()  # получение всех строк результата
    conn.close()  # закрытие соединения

    # Вычисление темпа прироста
    growth_rates = []
    for i in range(1, len(rows192)):
        current_value = rows192[i][0]
        previous_value = rows192[i-1][0]
        growth_rate = (current_value - previous_value) / previous_value
        growth_rates.append(growth_rate)

    rows = []
    id_indicator = 193
    for year, growth_rate in zip([row[1] for row in rows192[1:]], growth_rates):
        value_indicator = round(growth_rate * 100, 2)
        rows.append((value_indicator, year, True, datetime.now(), datetime.now(), id_indicator, id_territory))

    for row in rows:
        print(row)
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