from django.db import models

# Create your models here.
class Expenses(models.Model):
    time = models.DateField(verbose_name='Месяц')
    material = models.FloatField(max_length=30, verbose_name='Сырье и материалы, ₽', default=0)
    fot = models.FloatField(max_length=30, verbose_name='ФОТ, ₽', default=0)
    tool = models.FloatField(max_length=30, verbose_name='Затраты на инструмент, ₽', default=0)
    material_machine = models.FloatField(max_length=30, verbose_name='Материал для содержания оборудоания, ₽', default=0)
    repair = models.FloatField(max_length=30, verbose_name='Работы по ремонту и обслуживанию оборудования, ₽',default=0)
    oil = models.FloatField(max_length=30, verbose_name='Дециентрализованные масла и смазки, ₽', default=0)
    workwear = models.FloatField(max_length=30, verbose_name='Спецодежда, ₽', default=0)
    electricity = models.FloatField(max_length=30, verbose_name='Затраты на электроэнергию, ₽', default=0)
    depreciation = models.FloatField(max_length=30, verbose_name='Амортизация, ₽', default=0)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.time}"

    class Meta:
        db_table = "Expenses"
        verbose_name_plural = 'Расходы на месяц'


class Analog (models.Model):
    date = models.DateField(verbose_name='Месяц')
    price = models.FloatField(max_length=30, verbose_name='Стоимость, ₽', default=0)
    name = models.CharField(max_length=70, verbose_name='Наименование', null=True, blank=True)
    EAM = models.CharField(max_length=50, verbose_name='№ ЕАМ')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.EAM}: {self.price} - {self.date}"

    class Meta:
        db_table = "Analog"
        verbose_name_plural = 'Аналог'

class WAP (models.Model):
    date = models.DateField(verbose_name='Месяц')
    price = models.FloatField(max_length=30, verbose_name='Стоимость, ₽', default=0)
    analog= models.ForeignKey(Analog, on_delete=models.CASCADE, verbose_name='Аналог', null=True,
                                    blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.price} - {self.date}"

    class Meta:
        db_table = "WAP"
        verbose_name_plural = 'СВЦ'

class PriceArchive (models.Model):
    application = models.ForeignKey(Analog, on_delete=models.CASCADE, verbose_name='Заявка')
    wap = models.ForeignKey(Analog, on_delete=models.CASCADE, verbose_name='СВЦ')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.application}"

    class Meta:
        db_table = "PriceArchive"
        verbose_name_plural = 'Архиф цен'