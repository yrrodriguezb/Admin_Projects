from django import forms
from django.contrib.auth.models import User 
from .models import Client, SocialNetwork

# Constantes
ERROR_MESSAGE_USER = { 
    'required': 'El usuario es requerido',
    'unique': 'El usuario ya esta registrado',
    'invalid': 'El nombre de usuario es incorrecto'    
}

ERROR_MESSAGE_PASSWORD = { 
    'required': 'La contraseña es requerida' 
}

ERROR_MESSAGE_EMAIL = {
    'invalid': 'Ingrese un correo valido'
}


def must_be_gt(value_password):
    if len(value_password) < 5:
        raise forms.ValidationError('El password debe tener mas de 5 caracteres')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def __init__(self):
        super(LoginForm, self).__init__()
        self.fields['username'].widget.attrs.update({ 'id': 'username_login',  'class': 'input_login' })
        self.fields['password'].widget.attrs.update({ 'id': 'password_login', 'class': 'input_login' })


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20, error_messages = ERROR_MESSAGE_USER)
    password: forms.CharField(max_length=20, error_messages = ERROR_MESSAGE_PASSWORD, widget=forms.PasswordInput())
    email = forms.CharField(error_messages= ERROR_MESSAGE_EMAIL)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({ 'id': 'username_create' })
        self.fields['password'].widget.attrs.update({ 'id': 'password_create' })
        self.fields['email'].widget.attrs.update({ 'id': 'password_create' })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count():
            raise forms.ValidationError('El email ya existe.')

        return email
        
    class Meta:
        model = User

        fields = (
            'username',
            'password',
            'email'
        )


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20, error_messages=ERROR_MESSAGE_USER)
    email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)
    first_name = forms.CharField(label='Nombre completo', required=False)
    last_name = forms.CharField(label='Apellidos', required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.id).count():
            raise forms.ValidationError('El email ya existe.')

        return email

class EditUserPasswordForm(forms.Form):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])
    new_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])

    def clean(self):
        clean_data = super(EditUserPasswordForm, self).clean()
        pass1 = clean_data.get('new_password')
        pass2 = clean_data.get('repeat_password')

        if pass1 != pass2:
            raise forms.ValidationError('Las contraseñas no son iguales')


class EditClientForm(forms.ModelForm):
    job = forms.CharField(label='Trabajo Actual', required=False)
    bio = forms.CharField(label='Biografía', widget=forms.Textarea(), required=False)

    class Meta:
        model = Client
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(EditClientForm, self).__init__(*args, **kwargs)
        self.fields['job'].widget.attrs.update({ 'id': 'job_edit_client', 'class': 'validate' })
        self.fields['bio'].widget.attrs.update({ 'id': 'bio_edit_client', 'class': 'validate' })


class EditClientSocialForm(forms.ModelForm):
    class Meta:
        model = SocialNetwork
        exclude = ['user']