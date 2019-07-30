from django import forms
from status.models import Status

class StatusChoicesForm(forms.Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(), initial=0)

    def __init__(self, *args, **kwargs):
        super(StatusChoicesForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({ 'class': 'browser-default' })
