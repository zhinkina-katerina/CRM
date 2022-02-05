from django import forms


class TtnForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.ttn = kwargs.pop('ttn')
        super(TtnForm,self).__init__(*args,**kwargs)
        self.fields['ttn'].widget = forms.TextInput(attrs={'value': self.ttn})

    ttn = forms.CharField(label='ТТН')