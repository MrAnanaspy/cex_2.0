from django import forms
from django.core.validators import URLValidator
from .models import Milling, Plates


class MillingForm(forms.ModelForm):
    # Дополнительные поля, если нужно

    class Meta:
        model = Milling
        fields = [
            'name', 'quantity', 'image_url', 'attributes',
            'diameter', 'work_diameter', 'url_market', 'plates', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите наименование',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'id': 'tool-quantity',
                'min': '0'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com/images/tool.jpg',
                'id': 'photo-url'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Подробное описание инструмента, его назначение и особенности',
                'id': 'tool-description',
                'rows': 4
            }),
            'diameter': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'placeholder': 'Диаметр в мм'
            }),
            'work_diameter': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'placeholder': 'Фактический рабочий диаметр в мм'
            }),
            'url_market': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com/product'
            }),
            'plates': forms.Select(attrs={
                'class': 'form-input'
            }),
            'attributes': forms.HiddenInput(attrs={
                'id': 'attributes-field'
            }),
        }
        labels = {
            'name': 'Наименование',
            'quantity': 'Количество на складе',
            'image_url': 'Ссылка на фотографию',
            'description': 'Описание инструмента',
            'diameter': 'Диаметр',
            'work_diameter': 'Фактический рабочий диаметр',
            'url_market': 'Ссылка на магазин',
            'plates': 'Пластины',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если у экземпляра есть данные, заполняем поле title

        # Добавляем CSS классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'attributes':  # attributes скрытое поле
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-input'

        # Особые настройки для определенных полей
        self.fields['description'].widget.attrs.update({
            'class': 'form-textarea',
            'rows': 4
        })

        self.fields['plates'].widget.attrs.update({
            'class': 'form-input'
        })

    class MillingForm(forms.ModelForm):
        title = forms.CharField(
            max_length=100,
            label='Название инструмента',
            widget=forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название инструмента',
                'id': 'tool-name'
            }),
            required=False
        )

        class Meta:
            model = Milling
            fields = [
                'name', 'quantity', 'image_url', 'attributes',
                'diameter', 'work_diameter', 'url_market', 'plates', 'description'
            ]
            # ... остальные widgets и labels ...

        def clean_title(self):
            title = self.cleaned_data.get('title')
            if title:
                # Проверяем, существует ли фреза с таким названием (исключая текущую)
                existing = Milling.objects.filter(name__iexact=title)

                # Если редактируем существующую запись, исключаем ее из проверки
                if self.instance and self.instance.pk:
                    existing = existing.exclude(pk=self.instance.pk)

                if existing.exists():
                    raise forms.ValidationError(
                        f'Фреза с названием "{title}" уже существует. '
                        f'Выберите другое название.'
                    )

            return title

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if name:
                # Дублирующая проверка для поля name
                existing = Milling.objects.filter(name__iexact=name)

                if self.instance and self.instance.pk:
                    existing = existing.exclude(pk=self.instance.pk)

                if existing.exists():
                    raise forms.ValidationError(
                        f'Фреза с названием "{name}" уже существует.'
                    )

            return name


    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            try:
                URLValidator()(image_url)
            except forms.ValidationError:
                raise forms.ValidationError("Введите корректный URL адрес")
        return image_url

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("Количество не может быть отрицательным")
        return quantity

    def clean_diameter(self):
        diameter = self.cleaned_data.get('diameter')
        if diameter and diameter < 0:
            raise forms.ValidationError("Диаметр не может быть отрицательным")
        return diameter
