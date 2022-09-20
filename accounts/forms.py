from django.forms import ModelForm
from django.forms.widgets import CheckboxInput, DateInput, TextInput, TimeInput

from .models import ExcelInput, GlikProfileModel, PinList

import datetime

class GlikProfileForm(ModelForm):
    
    class Meta:
        model = GlikProfileModel    
        fields = ['name', 'date', 'room']

        widgets = {
            "name": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ФИО',
                'style': 'width: 750px'
            }),
            "date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата',
                'value': datetime.date.today()
            }),
            "room": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Палата'
            })
        }


class Water(ModelForm):
    
    class Meta:
        model = GlikProfileModel    
        fields = ['name', 'date', 'room']

        widgets = {
            "name": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Фамилия',
                'style': 'width: 750px'
            }),
            "date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата',
                'value': datetime.date.today()
            }),
            "room": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Палата'
            })
        }


class ExcelIn(ModelForm):
    
    class Meta:
        model = ExcelInput
        fields = ['file_in']

        widgets = {
            "file_in": TextInput(attrs={
                'type': 'file',
                'class': 'form-control',
                'placeholder': 'Выберите файл',
                # 'style': 'width: 750px'
            })
        }


class Pin(ModelForm):
    
    class Meta:
        model = PinList  
        fields = ['name', 'date', 'med', 'doctor', 'pvk_date', 'zvk_date', 'uk_date',
        'diabet', 'lite', 'belok', 'lite_belok', 'low_kallory', 'hight_kallory',
        'yes_no', 'deadline', 'n', 'one', 'two', 'chair']

        widgets = {
            "name": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ФИО пациента',
                'style': 'width: 750px'
            }),
            "med": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ФИО мед сестры',
                'style': 'width: 750px'
            }),
            "doctor": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ФИО доктора',
                'style': 'width: 750px'
            }),
            "date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата',
                'value': datetime.date.today(),
                'style': 'width: 160px'
            }),
            "pvk_date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата ПВК',
                'style': 'width: 160px'
            }),
            "zvk_date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата ЦВК',
                'style': 'width: 160px'
            }),
            "uk_date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата УК',
                'style': 'width: 160px'
            }),
            "deadline": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата окончания диеты',
                'style': 'width: 160px'
            }),
            "diabet": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "lite": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "belok": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "lite_belok": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "low_kallory": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "hight_kallory": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            })
            ,
            "yes_no": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "n": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "one": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "two": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            }),
            "chair": CheckboxInput(attrs={
                'type': "checkbox",
                'class': 'form-control',
                'style': 'width: 50px'
            })
        }
