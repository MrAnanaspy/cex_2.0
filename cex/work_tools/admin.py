from django.contrib import admin
from django.utils.html import format_html
from django.dispatch import receiver
from mptt.admin import MPTTModelAdmin

from .models import *


# Register your models here.
@admin.register(Milling)
class MillingAdmin(admin.ModelAdmin):
    pass

@admin.register(Drill)
class MillingAdmin(admin.ModelAdmin):
    pass