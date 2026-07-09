from django import forms
from .models import Operator, Machine, TimeStudy


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = '__all__'

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

class TimeStudyForm(forms.ModelForm):
    class Meta:
        model = TimeStudy
        fields = [
            'operator',
            'machine',
            'batch_no',
            'operation',
            'date',
            'reading1',
            'reading2',
            'reading3',
            'reading4',
            'reading5',
            'average',
            'allowance',
            'capacity'
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }