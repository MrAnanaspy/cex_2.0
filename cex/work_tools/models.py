from django.core.validators import URLValidator
from django.db import models

# Create your models here.
class Plates(models.Model):
    id = models.CharField(max_length=100, verbose_name='Наименование', primary_key=True)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[ URLValidator()],
        verbose_name="Ссылка на фото"
    )
    attributes = models.JSONField()
    radius = models.FloatField(verbose_name='диаметр', default=0)
    url_market = models.CharField(max_length=300, verbose_name='Ссылка на магазин', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.quantity}"

    class Meta:
        db_table = "Plates"
        verbose_name_plural = 'Пластины'


class Milling(models.Model):
    # Лучше использовать автоматический ID или UUID для primary_key
    id = models.AutoField(primary_key=True)  # Или models.UUIDField
    name = models.CharField(max_length=100, verbose_name='Наименование')  # Отдельное поле для имени
    id_monolit = models.CharField(max_length=100, verbose_name='Код монолита', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[URLValidator()],
        verbose_name="Ссылка на фото"
    )
    attributes = models.JSONField(default=dict)  # Добавлен default
    diameter = models.FloatField(verbose_name='Диаметр', default=0)  # Изменен на FloatField
    work_diameter = models.FloatField(verbose_name='Фактический рабочий диаметр', default=0)
    url_market = models.URLField(max_length=300, verbose_name='Ссылка на магазин', null=True, blank=True)  # Изменен на URLField
    plates = models.ForeignKey('Plates', on_delete=models.SET_NULL, verbose_name='Пластины', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    storage_location = models.TextField(verbose_name='Место хранения', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}"

    @property
    def model_verbose_name(self):
        return self._meta.verbose_name_plural

    class Meta:
        db_table = "Milling"
        verbose_name_plural = 'Фрезы'

class Drill(models.Model):
    # Лучше использовать автоматический ID или UUID для primary_key
    id = models.AutoField(primary_key=True)  # Или models.UUIDField
    name = models.CharField(max_length=100, verbose_name='Наименование')  # Отдельное поле для имени
    id_monolit = models.CharField(max_length=100, verbose_name='Код монолита', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[URLValidator()],
        verbose_name="Ссылка на фото"
    )
    attributes = models.JSONField(default=dict)  # Добавлен default
    diameter = models.FloatField(verbose_name='Диаметр', default=0)  # Изменен на FloatField
    work_diameter = models.FloatField(verbose_name='Фактический рабочий диаметр', default=0)
    url_market = models.URLField(max_length=300, verbose_name='Ссылка на магазин', null=True, blank=True)  # Изменен на URLField
    plates = models.ForeignKey('Plates', on_delete=models.SET_NULL, verbose_name='Пластины', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    storage_location = models.TextField(verbose_name='Место хранения', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}"

    @property
    def model_verbose_name(self):
        return self._meta.verbose_name_plural

    class Meta:
        db_table = "Drill"
        verbose_name_plural = 'Сверла'


