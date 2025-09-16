from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *


# Register your models here.
@admin.register(Branch)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Signature)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(EngineerWork)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(TechnologistWork)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Machine)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(MachineOperation)
class DetailAdmin(admin.ModelAdmin):
    pass


@admin.register(OperatorWork)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class DetailAdmin(MPTTModelAdmin):
    pass

@admin.register(Act)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(MSK)
class DetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Application)
class DetailAdmin(admin.ModelAdmin):
    pass