from django import forms


class PeriodSelectionForm(forms.Form):
    """Для формы выбора МО и периода воводы данных по показателям"""
    list_territories = [
        (1, 'Алтайский край'),
        (2, 'г.Алейск'),
        (3, 'г.Барнаул'),
        (4, 'г.Белокуриха'),
        (5, 'г.Бийск'),
        (6, 'г.Заринск'),
        (7, 'г.Змеиногорск'),
        (8, 'г.Камень-на-Оби'),
        (9, 'г.Новоалтайск'),
        (10, 'г.Рубцовск'),
        (11, 'г.Славгород'),
        (12, 'г.Яровое'),
        (182, 'ЗАТО Сибирский'),
        (13, 'Алейский район'),
        (14, 'Алтайский район'),
        (15, 'Баевский район'),
        (16, 'Бийский район'),
        (17, 'Благовещенский район'),
        (18, 'Бурлинский район'),
        (19, 'Быстроистокский район'),
        (20, 'Волчихинский район'),
        (21, 'Егорьевский район'),
        (22, 'Ельцовский район'),
        (23, 'Завьяловский район'),
        (24, 'Залесовский район'),
        (25, 'Заринский район'),
        (26, 'Змеиногорский район'),
        (27, 'Зональный район'),
        (28, 'Калманский район'),
        (29, 'Каменский район'),
        (30, 'Ключевский район'),
        (31, 'Косихинский район'),
        (32, 'Красногорский район'),
        (33, 'Краснощековский район'),
        (34, 'Крутихинский район'),
        (35, 'Кулундинский район'),
        (36, 'Курьинский район'),
        (37, 'Кытмановский район'),
        (38, 'Локтевский район'),
        (39, 'Мамонтовский район'),
        (40, 'Михайловский район'),
        (41, 'Немецкий район'),
        (42, 'Новичихинский район'),
        (43, 'Павловский район'),
        (44, 'Панкрушихинский район'),
        (45, 'Первомайский район'),
        (46, 'Петропавловский район'),
        (47, 'Поспелихинский район'),
        (48, 'Ребрихинский район'),
        (49, 'Родинский район'),
        (50, 'Романовский район'),
        (51, 'Рубцовский район'),
        (52, 'Славгородский район'),
        (53, 'Смоленский район'),
        (54, 'Советский район'),
        (55, 'Солонешенский район'),
        (56, 'Солтонский район'),
        (57, 'Суетский район'),
        (58, 'Табунский район'),
        (59, 'Тальменский район'),
        (60, 'Тогульский район'),
        (61, 'Топчихинский район'),
        (62, 'Третьяковский район'),
        (63, 'Троицкий район'),
        (64, 'Тюменцевский район'),
        (65, 'Угловский район'),
        (66, 'Усть-Калманский район'),
        (67, 'Усть-Пристанский район'),
        (68, 'Хабарский район'),
        (69, 'Целинный район'),
        (70, 'Чарышский район'),
        (71, 'Шелаболихинский район'),
        (72, 'Шипуновский район')
    ]
    territory_level = forms.ChoiceField(
        choices=list_territories,
        initial='Алтайский край',
    )

    date = [(i, i) for i in range(2011, 2023)]
    start_date = forms.ChoiceField(
        choices=date,
        initial=2018,
    )
    end_date = forms.ChoiceField(
        choices=date[5:],
        initial=2022,
    )
