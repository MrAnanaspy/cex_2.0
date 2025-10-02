from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=50, verbose_name='Филиал')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Branch"
        verbose_name_plural = 'Филиал'