from django import forms


class PeriodSelectionForm(forms.Form):
    """Для формы выбора периода воводы данных по показателям"""
    date = [(i, i) for i in range(2011, 2023)]
    start_date = forms.ChoiceField(
        choices=date,
        initial=2018,
    )
    end_date = forms.ChoiceField(
        choices=date[5:],
        initial=2022,
    )
