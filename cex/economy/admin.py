from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Expenses)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Analog)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(WAP)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(PriceArchive)
class DetailAdmin(admin.ModelAdmin):
    pass