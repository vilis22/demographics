from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import DemographicStatistics, Territories, Indicators
from .forms import PeriodSelectionForm
import json


def get_name_and_path_by_id(id123, file_path='demographics_monitor/map.json'):
    """Возвращает МО и координаты расположения на карте"""
    with open(file_path, 'r') as file:
        data123 = json.load(file)
    for item in data123:
        if item['id'] == id123:
            return item['name'], item['path']
    return None, None


def get_values_for_key(data, key, years):
    """Принимает имя ключа и список years, а затем возвращает список значений для этого ключа, добавляя пустые строки, если ключ отсутствует."""
    try:
        return [data[key]['values'][y] for y in years]
    except KeyError:
        return [''] * len(years)


menu = [
    {'title': "Концепция", 'url_name': 'concept'},
    {'title': "О платформе", 'url_name': 'platform'},
    {'title': "Новости", 'url_name': 'news'},
    {'title': "Контакты", 'url_name': 'contacts'},
]

section = [
    {
        'title': 'Численность и структура населения',
        'subitems': [
            {'title': 'Динамика и копоненты изменения численности населения', 'url_name': 'population'},
            {'title': 'Численность и структура населения в разрезе территорий', 'url_name': 'population'},
            {'title': 'Численность и состав населения по полу', 'url_name': 'population'},
            {'title': 'Численность и возрастная структура населения', 'url_name': 'population'},
        ]
    },
    {
        'title': 'Рождаемость',
        'subitems': [
            {'title': 'Динамика рождаемости и факторов, влияющих на нее', 'url_name': 'fertility'},
            {'title': 'Возрастная структура рождаемости', 'url_name': 'fertility'},
            {'title': 'Рождаемость по очередности рождений', 'url_name': 'fertility'},
            {'title': 'Прерывание беременности', 'url_name': 'fertility'},
        ]
    },
    {
        'title': 'Смертность',
        'subitems': [
            {'title': 'Основные показатели смертности и продолжительность жизни', 'url_name': 'mortality_main'},
            {'title': 'Возрастно-половая структура смерности населения', 'url_name': 'mortality_main'},
            {'title': 'Смертность по основным причинам смертности', 'url_name': 'mortality_main'},
        ]
    },
    {
        'title': 'Миграция',
        'subitems': [
            {'title': 'Динамика миграциии по типам', 'url_name': 'migration_threads'},
            {'title': 'Динамика миграции по полу', 'url_name': 'migration_gender'},
            {'title': 'Динамика миграции по возрастным группам', 'url_name': 'migration_age'},
            {'title': 'Динамика миграции по полу и возрастным группам', 'url_name': 'migration_gender_age'},
        ]
    },
    {
        'title': 'Браки и разводы',
        'subitems': [
            {'title': 'Основные показатели брачности и разводимости', 'url_name': 'marriages'},
        ]
    },
    {
        'title': 'Целевые показатели и прогноз',
        'subitems': [
            {'title': 'Дифференциация территорий по типам дем. развития', 'url_name': 'target'},
            {'title': 'Целевые индикаторы и степень их достижения', 'url_name': 'target'},
            {'title': 'Прогноз численности и структур населения', 'url_name': 'target'},
            {'title': 'Прогноз рождаемости', 'url_name': 'target'},
            {'title': 'Прогноз смертности', 'url_name': 'target'},
            {'title': 'Прогноз миграции', 'url_name': 'target'},
        ]
    },
]


def index(request):
    """Это стартовая страница"""
    data = {
        'title': 'Демографический мониторинг Алтайского края',
        'menu': menu,
        'section': section,
    }
    return render(request, "demographics_monitor/index.html", context=data)


def concept(request):
    """Концепция"""
    data = {
        'title': 'Концепция',
        'menu': menu,
    }
    return render(request, 'demographics_monitor/concept.html', context=data)


def platform(request):
    """О платформе"""
    data = {
        'title': 'О платформе',
        'menu': menu,
    }
    return render(request, 'demographics_monitor/platform.html', context=data)


def news(request):
    """Новости"""
    data = {
        'title': 'Новости',
        'menu': menu
    }
    return render(request, "demographics_monitor/news.html", context=data)


def contacts(request):
    """Контакты"""
    data = {
        'title': 'Контакты',
        'menu': menu
    }
    return render(request, "demographics_monitor/contacts.html", context=data)


def login(request):
    """Авторизация"""
    data = {
        'title': 'Авторизация',
        'menu': menu
    }
    return render(request, "demographics_monitor/login.html", context=data)


def target(request):
    """Целевые показатели и прогноз"""
    data = {
        'title': 'Целевые показатели и прогноз',
        'menu': menu,
        'section': section,
    }
    return render(request, "demographics_monitor/target.html", context=data)


def population(request):
    """Численность и структура населения"""
    data = {
        'title': 'Численность и структура населения',
        'menu': menu,
        'section': section,
    }
    return render(request, "demographics_monitor/population.html", context=data)


def fertility(request):
    """Рождаемость"""
    data = {
        'title': 'Рождаемость',
        'menu': menu,
        'section': section,
    }
    return render(request, "demographics_monitor/fertility.html", context=data)


def mortality_main(request):
    """Смертность. Основные показатели смертности и продолжительность жизни"""
    years = list(range(2018, 2023))
    territory_level = 1
    selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level),
                              None)

    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            territory_level = int(form.cleaned_data['territory_level'])
            selected_territory = next(
                (item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm

    if territory_level == 1:
        indicators = list(range(192, 198)) + [202] + list(range(205, 210)) + [212, 213]
        territories = [1, 74, 73]
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id__in=indicators,
            territory_id__in=territories,
            year__in=years
        ).order_by('indicator_id')
        data_by_indicator = {}
        list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами

        for data in data_last_three_years:
            if data.territory_id == 74:
                indicator_name = data.indicator.indicator_name + ' СФО'
            elif data.territory_id == 73:
                indicator_name = data.indicator.indicator_name + ' РФ'
            else:
                indicator_name = data.indicator.indicator_name
            unit_name = data.indicator.unit_measurement.unit_name

            if indicator_name not in data_by_indicator:
                data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}

            if data.indicator.unit_measurement.id in list_int_id:
                data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
            else:
                data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

        values = []
        data_last_three = Indicators.objects.filter(pk__in=indicators).order_by('pk')

        for data in data_last_three:
            values.append(get_values_for_key(data_by_indicator, data.indicator_name, years))

        """Список МО для рейтингов"""
        list_id_territory = list(range(2, 73)) + [182]
        middle_y = ['Яровое', 'Первомайский', 'Рубцовский', 'Егорьевский', 'Алейский']  # для оторбражения на карте, другие названия районов закрывают их

        """Темп прироста числа умерших"""
        municipalities_1 = []
        values_colors_1 = []
        colors_1 = ['#f6d4d4', '#eda9a9', '#e47f7f', '#db5454', '#d22929']
        map_1 = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=193,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('value')
        value_first = data_last_three_years.first()  # наименьшее значение
        value_first = float(value_first.value)
        value_last = data_last_three_years.last()  # наибольшее значение
        value_last = float(value_last.value)
        step = (value_last - value_first) / 5

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            municipalities_1.append(territory.territory_name)
            value_float = round(float(data.value), 1)
            color_index = min(int((value_float - value_first) / step), 4)
            values_colors_1.append({'y': value_float, 'color': colors_1[color_index]})
            name, path = get_name_and_path_by_id(str(territory.id))
            if name not in middle_y:
                map_1.append({"name": name, "path": path, "value": value_float})
            else:
                map_1.append({"name": name, "path": path, "value": value_float, "middleY": 0.25})

        """Общий коэффициент смертности"""
        municipalities_2 = []
        values_colors_2 = []
        map_2 = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=202,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('value')
        value_first = data_last_three_years.first()  # наименьшее значение
        value_first = float(value_first.value)
        value_last = data_last_three_years.last()  # наибольшее значение
        value_last = float(value_last.value)
        step = (value_last - value_first) / 5

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            municipalities_2.append(territory.territory_name)
            value_float = round(float(data.value), 1)
            color_index = min(int((value_float - value_first) / step), 4)
            values_colors_2.append({'y': value_float, 'color': colors_1[color_index]})
            name, path = get_name_and_path_by_id(str(territory.id))
            if name not in middle_y:
                map_2.append({"name": name, "path": path, "value": value_float})
            else:
                map_2.append({"name": name, "path": path, "value": value_float, "middleY": 0.25})

        context_data = {
            'title': 'Смертность. Основные показатели',
            'menu': menu,
            'section': section,
            'form': form,
            'data_by_indicator': data_by_indicator,
            'years': years,
            'selected_territory': selected_territory,
            'values': values,
            'municipalities_1': municipalities_1,
            'values_colors_1': values_colors_1,
            'municipalities_2': municipalities_2,
            'values_colors_2': values_colors_2,
            'map_1': map_1,
            'map_2': map_2,
        }
        return render(request, "demographics_monitor/mortality-main.html", context=context_data)
    else:
        return None


def migration_age(request):
    """Миграция. Динамика миграции по возрастным группам"""
    years = list(range(2018, 2023))
    territory_level = 1
    selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            territory_level = int(form.cleaned_data['territory_level'])
            selected_territory = next(
                (item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm

    indicators = list(range(303, 312)) + list(range(339, 348))
    data_last_three_years = DemographicStatistics.objects.filter(
        indicator_id__in=indicators,
        territory_id=territory_level,
        year__in=years
    ).order_by('indicator_id')
    data_by_indicator = {}
    list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами

    for data in data_last_three_years:
        indicator_name = data.indicator.indicator_name
        unit_name = data.indicator.unit_measurement.unit_name
        if indicator_name not in data_by_indicator:
            data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
        if data.indicator.unit_measurement.id in list_int_id:
            data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
        else:
            data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

    values = []
    data_last_three = Indicators.objects.filter(pk__in=indicators).order_by('pk')

    for data in data_last_three:
        values.append([data_by_indicator.get(data.indicator_name, {'values': [''] * len(years)})['values'][y] for y in years])

    context_data = {
        'title': 'Динамика миграции по возрастным группам',
        'menu': menu,
        'section': section,
        'form': form,
        'data_by_indicator': data_by_indicator,
        'years': years,
        'selected_territory': selected_territory,
        'values': values,
    }
    return render(request, "demographics_monitor/migration-age.html", context=context_data)


def migration_gender(request):
    """Миграция. Динамика миграции по полу"""
    years = list(range(2018, 2023))
    territory_level = 1
    selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            territory_level = int(form.cleaned_data['territory_level'])
            selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm

    indicators = list(range(312, 315)) + list(range(324, 327)) + list(range(348, 351)) + list(range(360, 363))
    data_last_three_years = DemographicStatistics.objects.filter(
        indicator_id__in=indicators,
        territory_id=territory_level,
        year__in=years
    ).order_by('indicator_id')
    data_by_indicator = {}
    list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами

    for data in data_last_three_years:
        indicator_name = data.indicator.indicator_name
        unit_name = data.indicator.unit_measurement.unit_name
        if indicator_name not in data_by_indicator:
            data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
        if data.indicator.unit_measurement.id in list_int_id:
            data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
        else:
            data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

    values = []
    data_last_three = Indicators.objects.filter(pk__in=indicators).order_by('pk')

    for data in data_last_three:
        values.append([data_by_indicator.get(data.indicator_name, {'values': [''] * len(years)})['values'][y] for y in years])

    context_data = {
        'title': 'Динамика миграции по полу',
        'menu': menu,
        'section': section,
        'form': form,
        'data_by_indicator': data_by_indicator,
        'years': years,
        'selected_territory': selected_territory,
        'values': values,
    }
    return render(request, "demographics_monitor/migration-gender.html", context=context_data)


def migration_gender_age(request):
    """Миграция. Динамика миграции по полу и возрасту"""
    years = list(range(2018, 2023))
    territory_level = 1
    selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            territory_level = int(form.cleaned_data['territory_level'])
            selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm

    indicators = list(range(315, 324)) + list(range(327, 336)) + list(range(351, 360)) + list(range(363, 372))
    data_last_three_years = DemographicStatistics.objects.filter(
        indicator_id__in=indicators,
        territory_id=territory_level,
        year__in=years
    ).order_by('indicator_id')
    data_by_indicator = {}
    list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами

    for data in data_last_three_years:
        indicator_name = data.indicator.indicator_name
        unit_name = data.indicator.unit_measurement.unit_name
        if indicator_name not in data_by_indicator:
            data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
        if data.indicator.unit_measurement.id in list_int_id:
            data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
        else:
            data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

    values = []
    data_last_three = Indicators.objects.filter(pk__in=indicators).order_by('pk')

    for data in data_last_three:
        values.append([data_by_indicator.get(data.indicator_name, {'values': [''] * len(years)})['values'][y] for y in years])

    context_data = {
        'title': 'Динамика миграции по полу и возрастным группам',
        'menu': menu,
        'section': section,
        'form': form,
        'data_by_indicator': data_by_indicator,
        'years': years,
        'selected_territory': selected_territory,
        'values': values,
    }
    return render(request, "demographics_monitor/migration-gender-age.html", context=context_data)


def migration_threads(request):
    """Миграция. Динамика миграции по типам"""
    years = list(range(2018, 2023))
    territory_level = 1
    selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)

    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            territory_level = int(form.cleaned_data['territory_level'])
            selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm

    if territory_level == 1:
        indicators = [300, 301, 302, 336, 337, 338] + list(range(372, 408))
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id__in=indicators,
            territory_id=territory_level,
            year__in=years
        ).order_by('indicator_id')
        data_by_indicator = {}
        list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами

        for data in data_last_three_years:
            indicator_name = data.indicator.indicator_name
            unit_name = data.indicator.unit_measurement.unit_name
            if indicator_name not in data_by_indicator:
                data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
            if data.indicator.unit_measurement.id in list_int_id:
                data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
            else:
                data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

        values = []
        data_last_three = Indicators.objects.filter(pk__in=indicators).order_by('pk')

        for data in data_last_three:
            values.append(get_values_for_key(data_by_indicator, data.indicator_name, years))

        """Формируем список субьектов РФ для рейтинга"""
        list_id_subjects = list(range(75, 157))
        subjects = []
        values_colors = []
        colors = ['#12617e', '#418198', '#71a0b2', '#a0c0cb', '#d0dfe5']
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=408,
            territory_id__in=list_id_subjects,
            year=years[-1]
        ).order_by('-value')
        value_first = data_last_three_years.first()  # наибольшее значение
        value_first = int(value_first.value)
        value_last = data_last_three_years.last()  # наименьшее значение
        value_last = int(value_last.value)
        step = (value_first - value_last) / 5

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            subjects.append(territory.territory_name)
            value = int(data.value)
            color_index = min(int((value_first - value) / step), 4)
            values_colors.append({'y': value, 'color': colors[color_index]})

        """Формируем список стран для рейтинга"""
        list_id_nations = list(range(157, 181)) + list(range(183, 226))
        nations = []
        values_colors_nations = []
        colors = ['#12617e', '#418198', '#71a0b2', '#a0c0cb', '#d0dfe5']
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=409,
            territory_id__in=list_id_nations,
            year=years[-1]
        ).order_by('-value')
        value_first = data_last_three_years.first()  # наибольшее значение
        value_first = int(value_first.value)
        value_last = data_last_three_years.last()  # наименьшее значение
        value_last = int(value_last.value)
        step = (value_first - value_last) / 5

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            nations.append(territory.territory_name)
            value = int(data.value)
            color_index = min(int((value_first - value) / step), 4)
            values_colors_nations.append({'y': value, 'color': colors[color_index]})

        """Формируем данные для карты"""
        list_id_territory = list(range(2, 73)) + [182]
        middle_y = ['Яровое', 'Первомайский', 'Рубцовский', 'Егорьевский', 'Алейский']  # для оторбражения на карте, другие названия районов закрывают их

        """Число прибывших (внутрикраевая миграция)"""
        arrivals_map = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=375,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('-value')

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            name, path = get_name_and_path_by_id(str(territory.id))
            value = int(data.value)
            if name not in middle_y:
                arrivals_map.append({"name": name, "path": path, "value": value})
            else:
                arrivals_map.append({"name": name, "path": path, "value": value, "middleY": 0.25})

        """Число выбывших (внутрикраевая миграция)"""
        departed_map = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=393,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('-value')

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            name, path = get_name_and_path_by_id(str(territory.id))
            value = int(data.value)
            if name not in middle_y:
                departed_map.append({"name": name, "path": path, "value": value})
            else:
                departed_map.append({"name": name, "path": path, "value": value, "middleY": 0.25})

        context_data = {
            'title': 'Динамика миграции по типам',
            'menu': menu,
            'section': section,
            'form': form,
            'data_by_indicator': data_by_indicator,
            'years': years,
            'selected_territory': selected_territory,
            'values': values,
            'subjects': subjects,
            'values_colors': values_colors,
            'nations': nations,
            'values_colors_nations': values_colors_nations,
            'arrivals_map': arrivals_map,
            'departed_map': departed_map,
        }
        return render(request, "demographics_monitor/migration-threads.html", context=context_data)
    else:
        """Данные по муниципальному образованию"""
        indicators = [300, 336, 372, 375, 378, 381, 384, 387, 390, 393, 396, 399, 402, 405]
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id__in=indicators,
            territory_id=territory_level,
            year__in=years
        ).order_by('indicator_id')
        data_by_indicator = {}
        list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами

        for data in data_last_three_years:
            indicator_name = data.indicator.indicator_name
            unit_name = data.indicator.unit_measurement.unit_name
            if indicator_name not in data_by_indicator:
                data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
            if data.indicator.unit_measurement.id in list_int_id:
                data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
            else:
                data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

        values = []
        data_last_three = Indicators.objects.filter(pk__in=indicators).order_by('pk')

        for data in data_last_three:
            values.append(get_values_for_key(data_by_indicator, data.indicator_name, years))

        context_data = {
            'title': 'Динамика миграции по типам',
            'menu': menu,
            'section': section,
            'form': form,
            'data_by_indicator': data_by_indicator,
            'years': years,
            'selected_territory': selected_territory,
            'values': values,
        }
        return render(request, "demographics_monitor/migration-threads-municipalities.html", context=context_data)


def marriages(request):
    """Браки и разводы. Основные показатели брасночти и разводимости """
    years = list(range(2018, 2023))
    territory_level = 1
    selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)

    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            territory_level = int(form.cleaned_data['territory_level'])
            selected_territory = next((item[1] for item in PeriodSelectionForm.list_territories if item[0] == territory_level), None)
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm

    if territory_level == 1:
        indicators = list(range(410, 431))
        territories = [1, 74, 73]
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id__in=indicators,
            territory_id__in=territories,
            year__in=years
        ).order_by('indicator_id')
        data_by_indicator = {}
        list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами
        for data in data_last_three_years:
            if data.territory_id == 74:
                indicator_name = data.indicator.indicator_name + ' СФО'
            elif data.territory_id == 73:
                indicator_name = data.indicator.indicator_name + ' РФ'
            else:
                indicator_name = data.indicator.indicator_name
            unit_name = data.indicator.unit_measurement.unit_name

            if indicator_name not in data_by_indicator:
                data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}

            if data.indicator.unit_measurement.id in list_int_id:
                data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
            else:
                data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)
        # values1 = [data_by_indicator['Число браков']['values'][y] if data_by_indicator['Число браков']['values'][y] != '' else '' for y in years]
        values1 = [data_by_indicator.get('Число браков', {'values': [''] * len(years)})['values'][y] for y in years]
        values2 = [data_by_indicator['Число разводов']['values'][y] if data_by_indicator['Число разводов']['values'][y] != '' else '' for y in years]
        values3 = [data_by_indicator['Индекс разводимости']['values'][y] if data_by_indicator['Индекс разводимости']['values'][y] != '' else '' for y in years]
        values4 = [data_by_indicator['Число браков в городской местности']['values'][y] if data_by_indicator['Число браков в городской местности']['values'][y] != '' else '' for y in years]
        values5 = [data_by_indicator['Число разводов в городской местности']['values'][y] if data_by_indicator['Число разводов в городской местности']['values'][y] != '' else '' for y in years]
        values6 = [data_by_indicator['Индекс разводимости в городской местности']['values'][y] if data_by_indicator['Индекс разводимости в городской местности']['values'][y] != '' else '' for y in years]
        values7 = [data_by_indicator['Число браков в сельской местности']['values'][y] if data_by_indicator['Число браков в сельской местности']['values'][y] != '' else '' for y in years]
        values8 = [data_by_indicator['Число разводов в сельской местности']['values'][y] if data_by_indicator['Число разводов в сельской местности']['values'][y] != '' else '' for y in years]
        values9 = [data_by_indicator['Индекс разводимости в сельской местности']['values'][y] if data_by_indicator['Индекс разводимости в сельской местности']['values'][y] != '' else '' for y in years]
        values10 = [data_by_indicator['Общий коэффициент брачности в городской местности']['values'][y] if data_by_indicator['Общий коэффициент брачности в городской местности']['values'][y] != '' else '' for y in years]
        values11 = [data_by_indicator['Общий К. разводимости в городской местности']['values'][y] if data_by_indicator['Общий К. разводимости в городской местности']['values'][y] != '' else '' for y in years]
        values12 = [data_by_indicator['Общий коэффициент брачности в сельской местности']['values'][y] if data_by_indicator['Общий коэффициент брачности в сельской местности']['values'][y] != '' else '' for y in years]
        values13 = [data_by_indicator['Общий К. разводимости в сельской местности']['values'][y] if data_by_indicator['Общий К. разводимости в сельской местности']['values'][y] != '' else '' for y in years]
        values14 = [data_by_indicator['Общий коэффициент брачности']['values'][y] if data_by_indicator['Общий коэффициент брачности']['values'][y] != '' else '' for y in years]
        values15 = [data_by_indicator['Общий коэффициент разводимости']['values'][y] if data_by_indicator['Общий коэффициент разводимости']['values'][y] != '' else '' for y in years]

        """ Сформируем список МО для 3х рейтингов """
        list_id_territory = list(range(2, 73)) + [182]
        middle_y = ['Яровое', 'Первомайский', 'Рубцовский', 'Егорьевский', 'Алейский']  # для оторбражения на карте, другие названия районов закрывают их

        # Общий коэффициент брачности
        municipalities_1 = []
        values_colors_1 = []
        colors_1 = ['#12617e', '#418198', '#71a0b2', '#a0c0cb', '#d0dfe5']
        marriage_map = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=416,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('-value')
        value_first = data_last_three_years.first()  # наибольшее значение
        value_first = float(value_first.value)
        value_last = data_last_three_years.last()  # наименьшее значение
        value_last = float(value_last.value)
        step = (value_first - value_last) / 5

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            municipalities_1.append(territory.territory_name)
            value_float = round(float(data.value), 1)
            color_index = min(int((value_first - value_float) / step), 4)
            values_colors_1.append({'y': value_float, 'color': colors_1[color_index]})
            name, path = get_name_and_path_by_id(str(territory.id))
            if name not in middle_y:
                marriage_map.append({"name": name, "path": path, "value": value_float})
            else:
                marriage_map.append({"name": name, "path": path, "value": value_float, "middleY": 0.25})

        # Общий коэффициент разводимости
        municipalities_2 = []
        values_colors_2 = []
        colors_2 = ['#f6d4d4', '#eda9a9', '#e47f7f', '#db5454', '#d22929']
        divorces_coefficient_map = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=419,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('value')
        value_first = data_last_three_years.first()  # наименьшее значение
        value_first = float(value_first.value)
        value_last = data_last_three_years.last()  # наибольшее значение
        value_last = float(value_last.value)
        step = (value_last - value_first) / 5

        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            municipalities_2.append(territory.territory_name)
            value_float = round(float(data.value), 1)
            color_index = min(int((value_float - value_first) / step), 4)
            values_colors_2.append({'y': value_float, 'color': colors_2[color_index]})
            name, path = get_name_and_path_by_id(str(territory.id))
            if name not in middle_y:
                divorces_coefficient_map.append({"name": name, "path": path, "value": value_float})
            else:
                divorces_coefficient_map.append({"name": name, "path": path, "value": value_float, "middleY": 0.25})

        # Индекс разводимости
        municipalities_3 = []
        values_colors_3 = []
        divorces_index_map = []
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id=422,
            territory_id__in=list_id_territory,
            year=years[-1]
        ).order_by('value')
        value_first = data_last_three_years.first()  # наибольшее значение
        value_first = float(value_first.value)
        value_last = data_last_three_years.last()  # наименьшее значение
        value_last = float(value_last.value)
        step = (value_last - value_first) / 5
        for data in data_last_three_years:
            territory = Territories.objects.get(pk=data.territory_id)
            municipalities_3.append(territory.territory_name)
            value_float = round(float(data.value), 1)
            color_index = min(int((value_float - value_first) / step), 4)
            values_colors_3.append({'y': value_float, 'color': colors_2[color_index]})
            name, path = get_name_and_path_by_id(str(territory.id))
            if name not in middle_y:
                divorces_index_map.append({"name": name, "path": path, "value": value_float})
            else:
                divorces_index_map.append({"name": name, "path": path, "value": value_float, "middleY": 0.25})

        context_data = {
            'title': 'Браки и разводы',
            'menu': menu,
            'section': section,
            'form': form,
            'data_by_indicator': data_by_indicator,
            'years': years,
            'values1': values1,
            'values2': values2,
            'values3': values3,
            'values4': values4,
            'values5': values5,
            'values6': values6,
            'values7': values7,
            'values8': values8,
            'values9': values9,
            'values10': values10,
            'values11': values11,
            'values12': values12,
            'values13': values13,
            'values14': values14,
            'values15': values15,
            'municipalities_1': municipalities_1,
            'values_colors_1': values_colors_1,
            'municipalities_2': municipalities_2,
            'values_colors_2': values_colors_2,
            'municipalities_3': municipalities_3,
            'values_colors_3': values_colors_3,
            'marriage_map': marriage_map,
            'divorces_coefficient_map': divorces_coefficient_map,
            'divorces_index_map': divorces_index_map,
        }
        return render(request, "demographics_monitor/marriages.html", context=context_data)
    else:
        # Данные по муниципальному образованию
        indicators = [410, 413, 416, 419, 422]
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id__in=indicators,
            territory_id=territory_level,
            year__in=years
        ).order_by('indicator_id')
        data_by_indicator = {}
        list_int_id = [4, 6, 9, 10]  # id единиц измерения, для которых значения являются целыми числами
        for data in data_last_three_years:
            indicator_name = data.indicator.indicator_name
            unit_name = data.indicator.unit_measurement.unit_name
            if indicator_name not in data_by_indicator:
                data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}

            if data.indicator.unit_measurement.id in list_int_id:
                data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
            else:
                data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)
        # Данные по краю
        indicators = [417, 418, 420, 421, 423, 424]
        data_last_three_years = DemographicStatistics.objects.filter(
            indicator_id__in=indicators,
            territory_id=1,
            year__in=years
        ).order_by('indicator_id')

        for data in data_last_three_years:
            indicator_name = data.indicator.indicator_name
            unit_name = data.indicator.unit_measurement.unit_name
            if indicator_name not in data_by_indicator:
                data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
            data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)

        # values1 = [data_by_indicator['Число браков']['values'][y] if data_by_indicator['Число браков']['values'][y] != '' else '' for y in years]
        # values2 = [data_by_indicator['Число разводов']['values'][y] if data_by_indicator['Число разводов']['values'][y] != '' else '' for y in years]
        # values3 = [data_by_indicator['Индекс разводимости']['values'][y] if data_by_indicator['Индекс разводимости']['values'][y] != '' else '' for y in years]
        # values4 = [data_by_indicator['Общий коэффициент брачности']['values'][y] if data_by_indicator['Общий коэффициент брачности']['values'][y] != '' else '' for y in years]
        # values5 = [data_by_indicator['Общий коэффициент разводимости']['values'][y] if data_by_indicator['Общий коэффициент разводимости']['values'][y] != '' else '' for y in years]
        # values1, values2, values3, values4, values5 = [], [], [], [], []
        values1 = get_values_for_key(data_by_indicator, 'Число браков', years)
        values2 = get_values_for_key(data_by_indicator, 'Число разводов', years)
        values3 = get_values_for_key(data_by_indicator, 'Индекс разводимости', years)
        values4 = get_values_for_key(data_by_indicator, 'Общий коэффициент брачности', years)
        values5 = get_values_for_key(data_by_indicator, 'Общий коэффициент разводимости', years)


        values6 = [data_by_indicator['Общий коэффициент брачности в городской местности']['values'][y] if data_by_indicator['Общий коэффициент брачности в городской местности']['values'][y] != '' else '' for y in years]
        values7 = [data_by_indicator['Общий коэффициент брачности в сельской местности']['values'][y] if data_by_indicator['Общий коэффициент брачности в сельской местности']['values'][y] != '' else '' for y in years]
        values8 = [data_by_indicator['Общий К. разводимости в городской местности']['values'][y] if data_by_indicator['Общий К. разводимости в городской местности']['values'][y] != '' else '' for y in years]
        values9 = [data_by_indicator['Общий К. разводимости в сельской местности']['values'][y] if data_by_indicator['Общий К. разводимости в сельской местности']['values'][y] != '' else '' for y in years]
        values10 = [data_by_indicator['Индекс разводимости в городской местности']['values'][y] if data_by_indicator['Индекс разводимости в городской местности']['values'][y] != '' else '' for y in years]
        values11 = [data_by_indicator['Индекс разводимости в сельской местности']['values'][y] if data_by_indicator['Индекс разводимости в сельской местности']['values'][y] != '' else '' for y in years]
        context_data = {
            'title': 'Браки и разводы',
            'menu': menu,
            'section': section,
            'form': form,
            'data_by_indicator': data_by_indicator,
            'years': years,
            'selected_territory': selected_territory,
            'values1': values1,
            'values2': values2,
            'values3': values3,
            'values4': values4,
            'values5': values5,
            'values6': values6,
            'values7': values7,
            'values8': values8,
            'values9': values9,
            'values10': values10,
            'values11': values11,
        }
        return render(request, "demographics_monitor/marriages-municipalities.html", context=context_data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена</h1>")
