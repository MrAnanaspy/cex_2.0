from django import template

register = template.Library()
print("=== model_tags loaded ===")
@register.filter(name='get_verbose_name_plural')
def get_verbose_name_plural(obj):
    """Возвращает verbose_name_plural модели объекта"""
    try:
        return obj._meta.verbose_name_plural
    except AttributeError:
        return ""

@register.filter(name='get_verbose_name')
def get_verbose_name(obj):
    """Возвращает verbose_name модели объекта"""
    try:
        return obj._meta.verbose_name
    except AttributeError:
        return ""