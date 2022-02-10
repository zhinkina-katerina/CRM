from django import forms
from .models import Order


class OrderDetailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if 'ttn' in kwargs:
            self.ttn = kwargs.pop('ttn')
        if 'status' in kwargs:
            self.status = kwargs.pop('status')
        if 'initial_is_disloyal' in kwargs:
            self.is_disloyal = kwargs.pop('is_disloyal')
        if 'is_paid_delivery' in kwargs:
            self.is_paid_delivery = kwargs.pop('is_paid_delivery')

        super(OrderDetailForm, self).__init__(*args, **kwargs)
        self.fields['ttn'].widget = forms.TextInput(attrs={'value': self.ttn})
        self.fields['status'].initial = self.initial_status
        self.fields['is_disloyal'].initial = self.initial_is_disloyal
        self.fields['is_paid_delivery'].initial = self.initial_is_paid_delivery


    ttn = forms.CharField(label='ТТН')
    status = forms.CharField(
        widget=forms.Select(choices=Order.STATUS_CHOICES,
                            attrs={'class': "btn btn-primary dropdown-toggle",
                                   'data-toggle': "dropdown",
                                   'aria-expanded': "false",
                                   'type': "button",
                                   'style': "background-color: #4f2170; "
                                            "border-color: #4f2170;"},
                            ))
    is_disloyal = forms.CharField(widget=forms.CheckboxInput(attrs={'style': "width: 17px;"
                                                                             "height: 15px;"
                                                                    }))
    is_paid_delivery = forms.CharField(widget=forms.CheckboxInput(attrs={'style': "width: 17px;"
                                                                                  "height: 15px;"
                                                                         }))


class StatusOfOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
