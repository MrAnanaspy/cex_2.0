from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import AllMaterials, ShapeMaterials


class AddMaterial(forms.Form):
    stamp = forms.ModelChoiceField(
        queryset=AllMaterials.objects.all(),
        empty_label="Выбери марку"
    )
    type = forms.ModelChoiceField(
        queryset=ShapeMaterials.objects.all(),
        empty_label="Выбири тип"
    )
    size = forms.CharField(help_text='Размер')
    initial_weight = forms.FloatField(help_text='Материала всего, кг')
    certificate = forms.CharField(help_text='№ Сертификата')
    melting = forms.CharField(help_text='№ Плавки')
    batch = forms.CharField(help_text='№ Партии')
    place = forms.CharField(help_text='Место')

    def clean_id(self):
        data = self.cleaned_data['stamp']

        if data < 0:
            raise ValidationError(_('Invalid date - значение не может быть меньше ноля'))

        return data