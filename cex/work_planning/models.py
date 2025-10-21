from django.contrib.auth.models import User, Group
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from storage_details.models import Detail, Specification
from warehouse_materials.models import WarehouseMaterial, WarehouseMaterial3D
from economy.models import PriceArchive
from branch.models import Branch

# Create your models here.

class Signature(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа', null=True, blank=True)
    date = models.DateField( verbose_name='Дата выполнения', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date}"

    class Meta:
        db_table = "Signature"
        verbose_name_plural = 'Подписи'

class EngineerWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    date_start = models.DateField( verbose_name='Дата выполнения', null=True, blank=True)
    date_end = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE, verbose_name='Подписи', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date_end}"

    class Meta:
        db_table = "EngineerWork"
        verbose_name_plural = 'Работа конструктора'

class TechnologistWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    date_start = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    date_end = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    print = models.BooleanField(verbose_name='Подписи', default=False)

    def __str__(self):
        return f"{self.user} - {self.date_end}"

    class Meta:
        db_table = "TechnologistWork"
        verbose_name_plural = 'Работа технолога'


class Machine(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название')
    type = models.CharField(max_length=70, verbose_name='Тип')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал', null=True, blank=True)
    technical_specifications = models.TextField(verbose_name='Технические характеристики', null=True, blank=True)
    break_down = models.DateField(verbose_name='Дата поломки', null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.name}"

    class Meta:
        db_table = "Machine"
        verbose_name_plural = 'Станки'

class MachineOperation(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Машина', null=True, blank=True)
    time_work = models.IntegerField(verbose_name='Время работы', null=True, blank=True)
    downtime = models.IntegerField(verbose_name='Время простоя', null=True, blank=True)

    def __str__(self):
        return f"{self.machine}"

    class Meta:
        db_table = "MachineOperation"
        verbose_name_plural = 'Работа станка'


class OperatorWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Оператор', null=True, blank=True)
    quantity_done = models.IntegerField(verbose_name='Количество выполнено', default=0)
    quantity_defect = models.IntegerField(verbose_name='Количество брака', default=0)
    date = models.DateField(verbose_name='Дата', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.quantity_done}/{self.quantity_defect}"

    class Meta:
        db_table = "OperatorWork"
        verbose_name_plural = 'Работа оператора'


class Task(MPTTModel):
    TYPE = (
        ('machine', 'Работа станка'),
        ('Handmade work', 'Ручная работа'),
        ('OTK', 'ОТК'),
    )
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа', null=True, blank=True)
    date_start = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    date_end = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    quantity_plan = models.IntegerField(max_length=30, verbose_name='Кол-во', default=0)
    quantity_actual = models.IntegerField(max_length=30, verbose_name='Кол-во', default=0)
    quantity_defect = models.IntegerField(max_length=30, verbose_name='Кол-во', default=0)
    task_txt = models.TextField(verbose_name= 'Текст задачи')
    type_task = models.CharField(max_length=30, choices=TYPE, verbose_name='Тип задачи', default=3)
    machine_operation = models.ForeignKey(MachineOperation, on_delete=models.CASCADE, verbose_name='Работа станка', null=True, blank=True)
    operator_work = models.ForeignKey(OperatorWork, on_delete=models.CASCADE, verbose_name='Работа оператора', null=True, blank=True)

    def __str__(self):
        return f"{self.group}"

    class Meta:
        db_table = "Tasks"
        verbose_name_plural = 'Задачи'


class Act(models.Model):
    TYPE = (
        ('approval', 'Согласен'),
        ('under_consideration', 'на рассмотрении'),
        ('disagree', 'Не согласен'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача', null=True, blank=True)
    incongruity_KD = models.TextField(verbose_name='Несоответствие по КД', null=True, blank=True)
    incongruity_fact = models.TextField(verbose_name='Несоответствие по факту', null=True, blank=True)
    controller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Контралер', null=True, blank=True, related_name = 'controller')
    perpetrator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Виновный', null=True, blank=True)
    reason = models.TextField(verbose_name='Причина несоответствия', null=True, blank=True)
    approval_perpetrator = models.CharField(max_length=30, choices=TYPE, verbose_name='Подпись виновного', default='under_consideration')
    conclusion_engineer = models.TextField(verbose_name='Заключение конструктора', null=True, blank=True)
    conclusion_technologist = models.TextField(verbose_name='Заключение технолога', null=True, blank=True)
    conclusion_main_engineer = models.TextField(verbose_name='Заключение главного конструктора', null=True, blank=True)
    final_decision = models.TextField(verbose_name='Заключение главного конструктора', null=True, blank=True)
    quantity_defect = models.IntegerField(verbose_name='Кол-во брака', default=0)
    quantity_correctable_defect = models.IntegerField(verbose_name='Кол-во исправляемого брака', default=0)
    time_correction = models.IntegerField(verbose_name='Время на исправление, мин', default=0)
    date_end = models.DateField(verbose_name='Дата закрытия', null=True, blank=True)

    def __str__(self):
        return f"{self.task}"

    class Meta:
        db_table = "Act"
        verbose_name_plural = 'Акт'

class MSK(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача', null=True, blank=True)
    act = models.ForeignKey(Act, on_delete=models.CASCADE, verbose_name='Задача', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Кол-во', default=0)
    detail = models.ForeignKey(Specification, on_delete=models.CASCADE, verbose_name='Деталь', null=True, blank=True)
    print = models.BooleanField(verbose_name='Использование 3Д', default=False)
    material = models.ForeignKey(WarehouseMaterial, on_delete=models.CASCADE, verbose_name='Материал', null=True,
                                 blank=True)
    material_3d = models.ForeignKey(WarehouseMaterial3D, on_delete=models.CASCADE, verbose_name='Материал 3д',
                                    null=True, blank=True)
    date_start = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    date_end = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        db_table = "MSK"
        verbose_name_plural = 'МСК'


class Application(models.Model):
    URGENCY = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал', null=True, blank=True, related_name = 'branch')
    task = models.TextField(verbose_name='Задача к разработке', null=True, blank=True)
    quantity = models.IntegerField( verbose_name='Кол-во', default=0)
    date_create = models.DateField(verbose_name='Дата создания')
    date_start = models.DateField( verbose_name='Дата начала', null=True, blank=True)
    date_end = models.DateField( verbose_name='Дата окончания', null=True, blank=True)
    branch_work = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филтал выполнения', null=True, blank=True)
    weight_work_piece = models.FloatField(verbose_name='Вес заготовки, Кг', default=0)
    urgency = models.IntegerField(choices=URGENCY, verbose_name='Срочность', default=3)
    msk = models.ForeignKey(MSK, on_delete=models.CASCADE, verbose_name='МСК', null=True, blank=True)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, verbose_name='Спецификация', null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик', null=True, blank=True)
    work_engineer = models.ForeignKey(EngineerWork, on_delete=models.CASCADE, verbose_name='Работа инженера-конструктора', null=True, blank=True)
    work_technologist = models.ForeignKey(TechnologistWork, on_delete=models.CASCADE, verbose_name='Работа технолога', null=True, blank=True)
    price_archive = models.ForeignKey(PriceArchive, on_delete=models.CASCADE, verbose_name='Архиф стоимости ', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        db_table = "Application"
        verbose_name_plural = 'Заявка'
