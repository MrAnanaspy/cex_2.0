from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from branch.models import Branch


# Create your models here.
class MaterialCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()
    name = models.CharField(max_length=50, verbose_name='Категория материала', primary_key=True)


    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = "MaterialCategory"
        verbose_name_plural = 'Категория материала'

class AllMaterials(models.Model):
    stamp = models.CharField(max_length=50, verbose_name='Марка материала', primary_key=True)
    type = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, verbose_name='Категория', null=True, blank=True)
    density = models.FloatField(verbose_name='Плотность материала', default=0)
    description = TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return f"{self.stamp}"

    class Meta:
        db_table = "AllMaterials"
        verbose_name_plural = 'Марка материала'


class WarehouseMaterial(models.Model):
    stamp = models.ForeignKey(AllMaterials, on_delete=models.SET_NULL, verbose_name='Марка материала', null=True,
                              blank=True)
    type = models.CharField(max_length=50, verbose_name='Форма', null=True, blank=True)
    size = models.CharField(max_length=50, verbose_name='Размер', null=True, blank=True)
    initial_weight = models.FloatField(verbose_name='Материала всего, кг', null=True, blank=True)
    actual_weight = models.FloatField(verbose_name='Материала осталось, кг', null=True, blank=True)
    price = models.FloatField(verbose_name='Цена материала', null=True, blank=True)
    certificate = models.CharField(max_length=50, verbose_name='№ Сертификата', null=True, blank=True)
    melting  = models.CharField(max_length=50, verbose_name='№ Плавки', null=True, blank=True)
    batch = models.CharField(max_length=50, verbose_name='№ Партии', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал', null=True,
                              blank=True)
    place = models.TextField(verbose_name='Место', null=True, blank=True)

    def __str__(self):
        return f"{self.stamp} - {self.type} {self.size}"

    class Meta:
        db_table = "WarehouseMaterial"
        verbose_name_plural = 'Склад материала'

class WarehouseMaterial3D(models.Model):
    TYPE = (
        ('PLA ', 'PLA'),
        ('FDM ', 'FDM'),
    )
    name = models.CharField(max_length=100, verbose_name='Наименование', primary_key=True)
    type = models.CharField(max_length=50, choices=TYPE, verbose_name='Тип печати', null=True,
                                           blank=True)
    link_market = models.CharField(max_length=150, verbose_name='Ссылка на магазин',  null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.type}"

    class Meta:
        db_table = "WarehouseMaterial3D"
        verbose_name_plural = 'Склад материала 3Д'

class ManualDebits(models.Model):
    datetime = models.DateTimeField(verbose_name='Время изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Марка материала', null=True,
                              blank=True)
    material = models.ForeignKey(WarehouseMaterial, on_delete=models.CASCADE, verbose_name='Марка материала', null=True,
                              blank=True)
    quantity = models.FloatField(verbose_name='Кол-во материала в кг')

    def __str__(self):
        return f"{self.datetime} - {self.material}"

    class Meta:
        db_table = "ManualDebits"
        verbose_name_plural = 'История списаний'


