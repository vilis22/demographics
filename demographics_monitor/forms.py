from django import forms


class PeriodSelectionForm(forms.Form):
    YEAR_CHOICES = [(i, i) for i in range(2011, 2023)]
    start_date = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=2018,
    )
    end_date = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=2022,
    )
