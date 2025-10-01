from django.db import models

# Create your models here.
class AllMaterials(models.Model):
    stamp = models.CharField(max_length=50, verbose_name='Марка материала', primary_key=True)
    density = models.FloatField(verbose_name='Плотность материала')

    def __str__(self):
        return f"{self.stamp}"

    class Meta:
        db_table = "MaterialsAll"
        verbose_name_plural = 'Марка материала'

class ShapeMaterials(models.Model):
    shape = models.CharField(max_length=50, verbose_name='Форма материала', primary_key=True)

    def __str__(self):
        return f"{self.shape}"

    class Meta:
        db_table = "MaterialsShape"
        verbose_name_plural = 'Формы материала'


class WarehouseMaterial(models.Model):
    stamp = models.ForeignKey(AllMaterials, on_delete=models.CASCADE, verbose_name='Марка материала', null=True,
                              blank=True)
    type = models.ForeignKey(ShapeMaterials, on_delete=models.CASCADE, verbose_name='Форма материла', null=True,
                                    blank=True)
    size = models.CharField(max_length=50, verbose_name='Размер', null=True, blank=True)
    initial_weight = models.FloatField(max_length=50, verbose_name='Материала всего, кг', null=True, blank=True)
    actual_weight = models.FloatField(max_length=50, verbose_name='Материала осталось, кг', null=True, blank=True)
    certificate = models.CharField(max_length=50, verbose_name='№ Сертификата', null=True, blank=True)
    melting  = models.CharField(max_length=50, verbose_name='№ Плавки', null=True, blank=True)
    batch = models.CharField(max_length=50, verbose_name='№ Партии', null=True, blank=True)

    def __str__(self):
        return f"{self.stamp}"

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


