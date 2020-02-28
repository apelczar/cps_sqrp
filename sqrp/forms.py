from django import forms
from django.forms.widgets import NumberInput

class SQRPConfigForm(forms.Form):
    def __init__(self, label_dict, *args, **kwargs):
        super(SQRPConfigForm, self).__init__(*args, **kwargs)
        for label in label_dict:
            self.fields[label] = forms.IntegerField(
                label=label, 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))