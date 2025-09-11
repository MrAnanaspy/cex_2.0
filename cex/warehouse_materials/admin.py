from django.contrib import admin
from django.utils.html import format_html
from django.dispatch import receiver
from mptt.admin import MPTTModelAdmin

from .models import AllMaterials, ShapeMaterials, WarehouseMaterial, WarehouseMaterial3D


# Register your models here.
@admin.register(AllMaterials)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(ShapeMaterials)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(WarehouseMaterial)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(WarehouseMaterial3D)
class DetailAdmin(admin.ModelAdmin):
    pass

