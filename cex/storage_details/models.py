from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse
from warehouse_materials.models import AllMaterials, ShapeMaterials

# Create your models here.
def image_directory_path(instance, filename):
    return '{0}/img/{1}'.format(instance.id, filename)


class Detail(models.Model):
    DIVISION = (
        ('БФО ', 'БФО'),
        ('Варочный ', 'Варочный'),
        ('Розлив ', 'Розлив'),
        ('Солодовня ', 'Солодовня'),
        ('Котельня ', 'Котельня'),
        ('Другое ', 'Другое'),
    )
    EAM = (models.CharField(max_length=20, null=True, blank=True))
    name = (models.CharField(max_length=100, verbose_name='Название', null=True, blank=True))
    division = models.CharField(max_length=50, choices=DIVISION, verbose_name='Подразделение', null=True,
                                           blank=True)
    mater = models.ForeignKey(AllMaterials, on_delete=models.CASCADE, verbose_name='Марка материала', null=True, blank=True)
    shape_mater = models.ForeignKey(ShapeMaterials, on_delete=models.CASCADE, verbose_name='Форма материла', null=True, blank=True)
    billet_weight = (models.CharField
                (max_length=100, verbose_name='Вес заготовки', null=True, blank=True))
    photo = (models.ImageField
             (max_length=260, verbose_name='Ссылка на фото', upload_to=image_directory_path, null=True, blank=True))
    twt = models.FloatField(max_length=30, verbose_name='Время работы токарного станка на 1 шт (мин)', default=0)
    twd = models.FloatField(max_length=30, verbose_name='Время простоя токарного станка на 1 шт (мин)', default=0)
    mwt = models.FloatField(max_length=30, verbose_name='Время работы фрезерного станка на 1 шт (мин)', default=0)
    mwd = models.FloatField(max_length=30, verbose_name='Время простоя фрезерного станка на 1 шт (мин)', default=0)
    tmwt = models.FloatField(max_length=30, verbose_name='Время работы токарно-фрезерного станка на 1 шт (мин)', default=0)
    tmwd = models.FloatField(max_length=30, verbose_name='Время простоя токарно-фрезерного станка на 1 шт (мин)', default=0)
    ewt = models.FloatField(max_length=30, verbose_name='Время работы электроэррозии на 1 шт (мин)',
                             default=0)
    ewd = models.FloatField(max_length=30, verbose_name='Время простоя электроэррозии на 1 шт (мин)',
                             default=0)
    procurement_work = models.FloatField(max_length=30,
                                         verbose_name='Время потраченное на заготовительные операции (Пила, плазма) 1 шт (мин)',
                                         default=0)
    locksmith_operations = models.FloatField(max_length=30,
                                         verbose_name='Время потраченное на слесарные операции 1 шт (мин)', default=0)
    post_processing = models.FloatField(max_length=30,
                                         verbose_name='Время потраченное на постобработку 1 шт (мин)', default=0)
    technical_control = models.FloatField(max_length=30,
                                        verbose_name='Время потраченное на технический контроль 1 шт (мин)', default=0)
    packaging = models.FloatField(max_length=30,
                                          verbose_name='Время потраченное на упаковку 1 шт (мин)', default=0)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.EAM} - {self.name}"


    class Meta:
        db_table = "Detail"
        verbose_name_plural = 'Детали'


class MultiplierDetail(models.Model):
    multiplier = models.IntegerField(verbose_name='Множитель', default=1)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='Задача', null=True, blank=True)

    def __str__(self):
        return f"{self.multiplier} - {self.detail}"

    class Meta:
        db_table = "MultiplierDetail"
        verbose_name_plural = 'Множитель детали'


class MultiplierStandardProducts(models.Model):
    multiplier = models.IntegerField(verbose_name='Множитель', default=1)
    name = models.CharField(max_length=100, verbose_name='Наименование', null=True, blank=True)

    def __str__(self):
        return f"{self.multiplier} - {self.name}"

    class Meta:
        db_table = "MultiplierStandardProducts"
        verbose_name_plural = 'Множитель стандартных деталей'

class MultiplierPurchasedPproducts(models.Model):
    multiplier = models.IntegerField(verbose_name='Множитель', default=1)
    name = models.CharField(max_length=100, verbose_name='Наименование', null=True, blank=True)

    def __str__(self):
        return f"{self.multiplier} - {self.name}"

    class Meta:
        db_table = "MultiplierPurchasedPproducts"
        verbose_name_plural = 'Множитель заказных деталей'


class Specification(MPTTModel):
    DIVISION = (
        ('БФО ', 'БФО'),
        ('Варочный ', 'Варочный'),
        ('Розлив ', 'Розлив'),
        ('Солодовня ', 'Солодовня'),
        ('Котельня ', 'Котельня'),
        ('Другое ', 'Другое'),
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    multiplier_assembling = models.IntegerField(verbose_name='Множитель', default=1)
    EAM = (models.CharField(max_length=20, null=True, blank=True))
    name = (models.CharField(max_length=100, verbose_name='Название', null=True, blank=True))
    division = models.CharField(max_length=50, choices=DIVISION, verbose_name='Подразделение', null=True, blank=True)
    multiplier_detail = models.ForeignKey(MultiplierDetail, on_delete=models.CASCADE, verbose_name='Множитель детали', null=True, blank=True, related_name = 'multiplier')
    multiplier_standard_products = models.ForeignKey(MultiplierStandardProducts, on_delete=models.CASCADE, verbose_name='Множитель стандартных деталей', null=True,blank=True, related_name='multiplier')
    multiplier_purchased_products = models.ForeignKey(MultiplierPurchasedPproducts, on_delete=models.CASCADE, verbose_name='Множитель заказных деталей', null=True,blank=True, related_name='multiplier')
    photo = (models.ImageField
             (max_length=260, verbose_name='Ссылка на фото', upload_to=image_directory_path, null=True, blank=True))
    build  = models.FloatField(max_length=30,
                                        verbose_name='Время потраченное на технический контроль 1 шт (мин)', default=0)
    packaging = models.FloatField(max_length=30,
                                          verbose_name='Время потраченное на упаковку 1 шт (мин)', default=0)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.EAM} - {self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = "Specification"
        verbose_name_plural = 'Спецификация'
