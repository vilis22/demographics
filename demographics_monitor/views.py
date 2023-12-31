from django.shortcuts import render
from .models import DemographicStatistics
from .forms import PeriodSelectionForm


def index(request):
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
    indicators = [1, 2, 3, 4, 5, 6]
    data_last_three_years = DemographicStatistics.objects.filter(
        indicator_id__in=indicators,
        territory_id=1,
        year__in=years
    ).order_by('indicator_id')
    data_by_indicator = {}
    for data in data_last_three_years:
        indicator_name = data.indicator.indicator_name
        unit_name = data.indicator.unit_measurement.unit_name
        if indicator_name not in data_by_indicator:
            data_by_indicator[indicator_name] = {
                'unit': unit_name,
                'values': {year: '' for year in years}
            }
        data_by_indicator[indicator_name]['values'][data.year] = data.value
    values1 = [
        int(data_by_indicator['Число браков']['values'][y])
        if data_by_indicator['Число браков']['values'][y] != ''
        else ''
        for y in years
        ]
    values2 = [
        int(data_by_indicator['Число разводов']['values'][y])
        if data_by_indicator['Число разводов']['values'][y] != ''
        else ''
        for y in years
    ]
    context_data = {
        'form': form,
        'data_by_indicator': data_by_indicator,
        'years': years,
        'values1': values1,
        'values2': values2,
    }
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
