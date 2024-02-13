from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import DemographicStatistics
from .forms import PeriodSelectionForm

menu = [
    {'title': "Концепция", 'url_name': 'concept'},
    {'title': "О платформе", 'url_name': 'platform'},
    {'title': "Новости", 'url_name': 'news'},
    {'title': "Контакты", 'url_name': 'contacts'},
]

section = [
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
            {'title': 'Основные показатели смертности и продолжительность жизни', 'url_name': 'mortality'},
            {'title': 'Возрастно-половая структура смерности населения', 'url_name': 'mortality'},
            {'title': 'Смертность по основным причинам смертности', 'url_name': 'mortality'},
        ]
    },
    {
        'title': 'Миграция',
        'subitems': [
            {'title': 'Динамика миграции по территории', 'url_name': 'migration'},
            {'title': 'Динамика миграции по потокам', 'url_name': 'migration'},
            {'title': 'Структура миграции по потокам', 'url_name': 'migration'},
            {'title': 'Состав мигрантов по полу и основным возрастным группам', 'url_name': 'migration'},
            {'title': 'Возрастно-половой состав мигрантов по территориям', 'url_name': 'migration'},
        ]
    },
    {
        'title': 'Браки и разводы',
        'subitems': [
            {'title': 'Основные показатели брачности и разводимости', 'url_name': 'marriages'},
        ]
    },
]


def index(request):
    data = {
        'title': 'Демографический мониторинг',
        'menu': menu,
        'section': section,
    }
    return render(request, "demographics_monitor/index.html", context=data)


def concept(request):
    return HttpResponse("Концепция")


def platform(request):
    data = {
        'title': 'О платформе',
        'menu': menu,
    }
    return render(request, 'demographics_monitor/platform.html', context=data)


def news(request):
    return HttpResponse("Новости")


def contacts(request):
    return HttpResponse("Контакты")


def login(request):
    return HttpResponse("Войти")


def target(request):
    return HttpResponse("Целевые показатели и прогноз")


def population(request):
    return HttpResponse("Численность")


def fertility(request):
    return HttpResponse("Рождаемость")


def mortality(request):
    return HttpResponse("Смертность")


def migration(request):
    return HttpResponse("Миграция")


def marriages(request):
    """Обрабатывает HTTP-запрос и возвращает представление HTML."""
    years = [2020, 2021, 2022]
    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date + 1))
    else:
        form = PeriodSelectionForm
    """ indicators = list(range(410, 431)) """
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
    values1 = [data_by_indicator['Число браков']['values'][y] if data_by_indicator['Число браков']['values'][y] != '' else '' for y in years]
    values2 = [data_by_indicator['Число разводов']['values'][y] if data_by_indicator['Число разводов']['values'][y] != '' else '' for y in years]
    values3 = [data_by_indicator['Индекс разводимости']['values'][y] if data_by_indicator['Индекс разводимости']['values'][y] != '' else '' for y in years]
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
    }
    return render(request, "demographics_monitor/marriages.html", context=context_data)



def test_page(request):
    """Обрабатывает HTTP-запрос и возвращает представление HTML."""
    years = [2020, 2021, 2022]
    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date+1))
    else:
        form = PeriodSelectionForm
    """ indicators = list(range(410, 431)) """
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
    values1 = [data_by_indicator['Число браков']['values'][y] if data_by_indicator['Число браков']['values'][y] != '' else '' for y in years]
    values2 = [data_by_indicator['Число разводов']['values'][y] if data_by_indicator['Число разводов']['values'][y] != '' else '' for y in years]
    values3 = [data_by_indicator['Индекс разводимости']['values'][y] if data_by_indicator['Индекс разводимости']['values'][y] != '' else '' for y in years]
    context_data = {'form': form, 'data_by_indicator': data_by_indicator, 'years': years, 'values1': values1, 'values2': values2, 'values3': values3}
    return render(request, 'demographics_monitor/test_page.html', context=context_data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена</h1>")
