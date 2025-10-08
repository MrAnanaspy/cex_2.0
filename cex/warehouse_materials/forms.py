from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from mptt.forms import TreeNodeChoiceField
from .models import AllMaterials, MaterialCategory


class MaterialSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        if value:
            try:
                material = AllMaterials.objects.get(pk=value)
                # Добавляем data-атрибуты из модели
                if hasattr(material, 'density'):
                    option['attrs']['data-density'] = str(material.density)
                if hasattr(material, 'name'):
                    option['attrs']['data-name'] = material.name
            except AllMaterials.DoesNotExist:
                pass

        return option


class AddMaterial(forms.Form):
    stamp = forms.ModelChoiceField(
        queryset=AllMaterials.objects.all(),
        empty_label="Выбери марку",
        widget=MaterialSelect(attrs={
            'required': 'required',
            'id': 'stamp',
        })
    )
    type = forms.ChoiceField(
        help_text='форма',
        widget=forms.Select(attrs={
             'required': 'required',
             'id': 'type',
         }),
        choices=(
            ('', "Выберите тип"),
            ('sheet', "Лист"),
            ("rod", "Пруток (круг)"),
            ("tube", "Труба"),
            ('profile', "Профиль"),
            ("wire", "Проволока"),
            ("angle", "Уголок"),
        ))
    size = forms.CharField(
        help_text='Размер',
        widget=forms.TextInput(attrs={
            'class': 'preview-value',
            'id': 'previewValue',
        })
    )
    initial_weight = forms.FloatField(
        help_text='Материала всего, кг',
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': '0.00',
            'id': 'initial_weight',
            'step': '0.01',
            'min': '0',
        })

    )
    price = forms.FloatField(
        help_text='Цена всего, руб.',
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': '0.0',
            'id': 'price',
            'step': '0.1',
            'min': '0',
        })

    )
    certificate = forms.CharField(
        help_text='№ Сертификата',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: CERT-2023-001',
            'id': 'certificate',
            'required': 'required',
        })
    )
    melting = forms.CharField(
        help_text='№ Плавки',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: PL-230512',
            'id': 'melting',
            'required': 'required',
        })
    )
    batch = forms.CharField(
        help_text='№ Партии',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: P-2023-0456',
            'id': 'batch',
            'required': 'required',
        })
    )
    place = forms.CharField(
        help_text='Место',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: Секция А, Стеллаж 3',
            'id': 'place',
            'required': 'required',
        })
    )

    def clean_id(self):
        data = self.cleaned_data['stamp']

        if data != '':
            raise ValidationError(_('Invalid date - значение не может быть меньше ноля'))

        return data

class EditMaterial(forms.Form):
    stamp = forms.ModelChoiceField(
        queryset=AllMaterials.objects.all(),
        empty_label="Выбери марку",
        widget=MaterialSelect(attrs={
            'required': 'required',
            'id': 'stamp',
        })
    )
    type = forms.ChoiceField(
        help_text='форма',
        widget=forms.Select(attrs={
            'required': 'required',
            'id': 'type',
        }),
        choices=(
            ('', "Выберите тип"),
            ('Лист', "Лист"),
            ("Пруток (круг)", "Пруток (круг)"),
            ("Труба", "Труба"),
            ('Профиль', "Профиль"),
            ("Проволока", "Проволока"),
            ("Уголок", "Уголок"),
        ))
    size = forms.CharField(
        help_text='Размер',
        widget=forms.TextInput(attrs={
            'class': 'preview-value',
            'id': 'previewValue',
        })
    )
    initial_weight = forms.FloatField(
        help_text='Материала всего, кг',
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': '0.00',
            'id': 'initial_weight',
            'step': '0.01',
            'min': '0',
        })

    )
    actual_weight = forms.FloatField(
        help_text='Материала всего, кг',
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': '0.00',
            'id': 'initial_weight',
            'step': '0.01',
            'min': '0',
        })

    )
    price = forms.FloatField(
        help_text='Цена всего, руб.',
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': '0.0',
            'id': 'price',
            'step': '0.1',
            'min': '0',
        })

    )
    certificate = forms.CharField(
        help_text='№ Сертификата',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: CERT-2023-001',
            'id': 'certificate',
            'required': 'required',
        })
    )
    melting = forms.CharField(
        help_text='№ Плавки',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: PL-230512',
            'id': 'melting',
            'required': 'required',
        })
    )
    batch = forms.CharField(
        help_text='№ Партии',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: P-2023-0456',
            'id': 'batch',
            'required': 'required',
        })
    )
    place = forms.CharField(
        help_text='Место',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: Секция А, Стеллаж 3',
            'id': 'place',
            'required': 'required',
        })
    )

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


class MaterialStamp(forms.Form):
    stamp = forms.CharField(
        help_text='№ Партии',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Например: Алюминий 6061',
            'id': 'gradeName',
            'required': 'required',
        })
    )
    category = TreeNodeChoiceField(
        queryset=MaterialCategory.objects.all(),
        empty_label="Выбери категорию",
        widget=forms.Select(attrs={
            'required': 'required',
            'id': 'materialType',
            'class': "required",
        })
    )
    density = forms.FloatField(
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': '0.00',
            'id': 'density',
            'step': '0.001',
            'min': '0',
        }))
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Дополнительная информация о марке материала...',
            'id': 'description',
            'rows': "3",
        })
    )

class DeleteStamp(forms.Form):
    confirmation = forms.CharField(
        help_text='Введите слово удалить',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Введите слово удалить',
            'id': 'gradeName',
            'required': 'required',
        })
    )

    def clean_delete(self):
        data = self.cleaned_data['confirmation']
        print(data)
        if data != 'удалить' and data != 'Удалить':
            raise ValidationError(_('Invalid date - не верно написано удалить'))
        else:
            return True
