import os

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField
from django.utils.translation import gettext as _
from mptt.forms import TreeNodeMultipleChoiceField

from .models import Specification, Detail, MultiplierStandardProducts, MultiplierPurchasedPproducts

from django import forms
from mptt.forms import TreeNodeMultipleChoiceField
import os


class AddSpecification(forms.Form):
    EAM = forms.CharField(
        help_text='EAM',
        widget=forms.TextInput(attrs={
            'class': 'spec-number',
            'id': 'EamValue',
        })
    )
    name = forms.CharField(
        help_text='Название',
        widget=forms.TextInput(attrs={
            'class': 'spec-name',
            'id': 'nameValue',
        })
    )
    category = forms.ChoiceField(
        help_text='подразделение',
        widget=forms.Select(attrs={
            'required': 'required',
            'id': 'categoryValue',
        }),
        choices=(
            (None, '-----'),
            ('БФО', 'БФО'),
            ('Варочный', 'Варочный'),
            ('Розлив', 'Розлив'),
            ('Солодовня', 'Солодовня'),
            ('Котельня', 'Котельня'),
            ('Другое', 'Другое'),
        )
    )
    description = forms.CharField(
        help_text='описание',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'описание',
            'id': 'descriptionValue',
            'required': 'required',
        })
    )

    subcategories = ModelMultipleChoiceField(
        queryset=Specification.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'subcategories', 'name':'category'}),
        label="Подкатегории",
        required=False
    )
    details = ModelMultipleChoiceField(
        queryset=Detail.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'details', 'name': 'details'}),
        label="Детали",
        required=False
    )
    standart_details = ModelMultipleChoiceField(
        queryset=MultiplierStandardProducts.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'standart_details', 'name': 'standart_details'}),
        label="Стандартные детали",
        required=False
    )
    zakaz_details = ModelMultipleChoiceField(
        queryset=MultiplierPurchasedPproducts.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'zakaz_details', 'name': 'zakaz_details'}),
        label="Заказные детали",
        required=False
    )

    # Альтернативный подход - кастомная валидация
    def clean(self):
        cleaned_data = super().clean()
        # Валидацию множественных файлов делаем в view
        return cleaned_data

    def clean_id(self):
        data = self.cleaned_data['stamp']

        if data != '':
            raise ValidationError(_('Invalid date - значение не может быть меньше ноля'))

        return data

    def clean_type(self):
        type_value = self.cleaned_data['type']
        match type_value:
            case 'sheet':
                type_value = "Лист"
            case 'rod':
                type_value = "Пруток (круг)"
            case 'tube':
                type_value = "Труба"
            case 'profile':
                type_value = "Профиль"
            case 'wire':
                type_value = "Проволока"
            case 'angle':
                type_value = "Уголок"
        return type_value