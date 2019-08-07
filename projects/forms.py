
import datetime
from django import forms
from .models import Project, ProjectPermission


class ProjectCreateForm(forms.ModelForm):
    title = forms.CharField(label='Titulo', required=True)
    description = forms.CharField(label='Descripcíon', required=True, widget=forms.TextInput())
    dead_line = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Project
        fields = ('title', 'description', 'dead_line',)


class PermissionProjectForm(forms.Form):
    permission = forms.ModelChoiceField(
        queryset=ProjectPermission.objects.all(),
        initial=0
    )
