from django.shortcuts import render
from .models import DemographicStatistics
from .forms import PeriodSelectionForm


def index(request):
    """Обрабатывает HTTP-запрос и возвращает представление HTML."""
    """ years = [2020, 2021, 2022] """
    years = (2020, 2021, 2022)
    if request.method == "POST":
        form = PeriodSelectionForm(request.POST)
        if form.is_valid():
            start_date = int(form.cleaned_data['start_date'])
            end_date = int(form.cleaned_data['end_date'])
            years = list(range(start_date, end_date+1))
    else:
        form = PeriodSelectionForm
    """ indicators = list(range(410, 431)) """
    indicators = tuple(range(410, 431))
    territorys = (1, 74, 73)
    data_last_three_years = DemographicStatistics.objects.filter(indicator_id__in=indicators, territory_id__in=territorys, year__in=years).order_by('indicator_id')
    data_by_indicator = {}
    list_float_indicators = (
        'Общий коэффициент брачности',
        'Общий коэффициент брачности РФ',
        'Общий коэффициент брачности СФО',
        'Общий коэффициент брачности в городской местности',
        'Общий коэффициент брачности в сельской местности',
        'Общий коэффициент разводимости',
        'Общий коэффициент разводимости СФО',
        'Общий коэффициент разводимости РФ',
        'Общий К. разводимости в городской местности',
        'Общий К. разводимости в сельской местности',
        'Индекс разводимости',
        'Индекс разводимости СФО',
        'Индекс разводимости РФ',
        'Индекс разводимости в городской местности',
        'Индекс разводимости в сельской местности'
    )
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
        if indicator_name not in list_float_indicators:
            data_by_indicator[indicator_name]['values'][data.year] = int(data.value)
        else:
            data_by_indicator[indicator_name]['values'][data.year] = round(float(data.value), 1)
    values1 = [data_by_indicator['Число браков']['values'][y] if data_by_indicator['Число браков']['values'][y] != '' else '' for y in years]
    values2 = [data_by_indicator['Число разводов']['values'][y] if data_by_indicator['Число разводов']['values'][y] != '' else '' for y in years]
    values3 = [data_by_indicator['Индекс разводимости']['values'][y] if data_by_indicator['Индекс разводимости']['values'][y] != '' else '' for y in years]
    context_data = {'form': form, 'data_by_indicator': data_by_indicator, 'years': years, 'values1': values1, 'values2': values2, 'values3': values3}
    return render(request, "demographics_monitor/index.html", context=context_data)


def about(request):
    """
    Отображает страницу "О сайте".
    Parameters
    ----------
    request : HttpRequest
        Входящий HTTP-запрос.
    Returns
    -------
    HttpResponse
        HTTP-ответ, который возвращает HTML-страницу "О сайте".
    """
    return render(request, 'demographics_monitor/about.html')
