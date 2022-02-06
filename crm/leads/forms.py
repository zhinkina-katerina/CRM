from django import forms
from django.forms import ModelForm
from .models import Order


class TtnForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.ttn = kwargs.pop('ttn')
        super(TtnForm, self).__init__(*args, **kwargs)
        self.fields['ttn'].widget = forms.TextInput(attrs={'value': self.ttn})

    ttn = forms.CharField(label='ТТН')


class StatusOfOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

        widgets = {
            'status': forms.Select(attrs={'class': "btn btn-primary dropdown-toggle",
                                          'data-toggle': "dropdown",
                                          'aria-expanded': "false",
                                          'type': "button",
                                          'style': "background-color: #4f2170; border-color: #4f2170;"},
                                   )
        }

    def __init__(self, *args, **kwargs):
        super(StatusOfOrderForm, self).__init__(*args, **kwargs)
        self.fields['status'].label = ""
