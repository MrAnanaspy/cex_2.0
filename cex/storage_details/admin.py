from django.contrib import admin
from django.utils.html import format_html
from django.dispatch import receiver
from mptt.admin import MPTTModelAdmin

from .models import *


# Register your models here.
@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('EAM', 'name',)

    def image_tag(self, obj):
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.photo.url))
    image_tag.short_description = 'Фото/Рендер'
    image_tag.allow_tags = True


@admin.register(MultiplierDetail)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(MultiplierStandardProducts)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(MultiplierPurchasedPproducts)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Specification)
class DetailAdmin(MPTTModelAdmin):
    pass