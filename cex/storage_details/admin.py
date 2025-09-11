from django.contrib import admin
from django.utils.html import format_html
from django.dispatch import receiver
from mptt.admin import MPTTModelAdmin

from .models import Detail, Post, Category


# Register your models here.
@admin.register(Detail)
class DetailAdmin(MPTTModelAdmin):
    list_display = ('EAM', 'name',)

    prepopulated_fields = {"slug": ("EAM",)}

    '''def image_tag(self, obj):
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.photo.url))
    image_tag.short_description = 'Фото/Рендер'
    image_tag.allow_tags = True
'''
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)


class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)