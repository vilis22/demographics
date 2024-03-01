from django.db import models


class UnitsMeasurement(models.Model):
    """
    Модель для хранения данных о единицах измерения.
    Attributes
    ----------
    unit_name : str
        Название единицы измерения.
    """
    unit_name = models.CharField(max_length=255)


class Territories(models.Model):
    """
    Модель для хранения данных об уровнях территории.
    Attributes:
        territory_name (str): Название уровня территории.
    """
    territory_name = models.CharField(max_length=255)


class Ministries(models.Model):
    """
    Модель для хранения данных о министерствах.
    Attributes:
        ministry_name (str): Название министерства.
    """
    ministry_name = models.CharField(max_length=255)


class Indicators(models.Model):
    """
    Модель для хранения данных о показателях.
    Attributes:
        indicator_name (str): Название показателя.
        unit_measurement (ForeignKey): Ссылка на единицу измерения.
        ministry (ForeignKey): Ссылка на министерство.
    """
    indicator_name = models.CharField(max_length=255)
    unit_measurement = models.ForeignKey(UnitsMeasurement, on_delete=models.CASCADE)
    ministry = models.ForeignKey(Ministries, on_delete=models.CASCADE)


class DemographicStatistics(models.Model):
    """
    Модель для хранения данных о значениях показателей.
    Attributes:
        indicator (ForeignKey): Ссылка на показатель.
        territory (ForeignKey): Ссылка на территорию.
        value (float): Значение показателя.
        year (int): Год, за который записан показатель.
        is_approved (bool): Статус утвержденных данных.
        time_create (datetime): Время создания записи.
        time_update (datetime): Время последнего обновления записи.
    """
    indicator = models.ForeignKey(Indicators, on_delete=models.CASCADE)
    territory = models.ForeignKey(Territories, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveSmallIntegerField()
    is_approved = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]  # Сортировка по умолчанию в обратном порядке
        indexes = [
            models.Index(fields=["-year"])  # индексируем поле для скорости работы
        ]
