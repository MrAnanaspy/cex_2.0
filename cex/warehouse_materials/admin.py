from django.contrib import admin
from django.utils.html import format_html
from django.dispatch import receiver
from mptt.admin import MPTTModelAdmin

from .models import AllMaterials, WarehouseMaterial, WarehouseMaterial3D, MaterialCategory


# Register your models here.
@admin.register(AllMaterials)
class AllMaterialsAdmin(admin.ModelAdmin):
    pass

@admin.register(MaterialCategory)
class MaterialCategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(WarehouseMaterial)
class WarehouseMaterialAdmin(admin.ModelAdmin):
    pass

@admin.register(WarehouseMaterial3D)
class WarehouseMaterial3DAdmin(admin.ModelAdmin):
    pass

