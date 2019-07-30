import json
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import (
    authenticate, 
    login as login_django, 
    logout as logout_django,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import View, CreateView, DetailView
from django.views.generic.edit import UpdateView

from .forms import (
    LoginForm, 
    CreateUserForm, 
    EditUserForm, 
    EditUserPasswordForm,
    EditClientForm,
    EditClientSocialForm
)

from .models import Client, SocialNetwork

    
def login(request):
    if request.user.is_authenticated:
        return redirect(to='client:dashboard')

    msg = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login_django(request, user) # Agrega el usuario a las variables de sesion
            return redirect(to='client:dashboard')
        else:
            message = 'Usuario incorrecto, verifca tus datos'

    form = LoginForm()
    context = { 
        'msg': msg,
        'form': form 
    }
    return render(request, "login.html", context)

@login_required(login_url='client:login')
def logout(request):
    logout_django(request)
    return redirect(to='client:login')

@login_required(login_url='client:login')
def dashboard(request):
    context = {
        'msg': 'Bienvenido'
    }
    return render(request, 'client/dashboard.html', context)

def create(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('client:login')

    context = {
        'form': form
    }
    return render(request, 'client/create.html', context)

@login_required(login_url='client:login')
def edit_password(request):
    form = EditUserPasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            current_password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            if authenticate(username=request.user.username, password=current_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Contraseña actualizada correctamente')
            else:
                messages.error(request, 'Contraseña no pudo ser actualizada')
    context = { 'form': form }
    return render(request, 'client/edit_password.html', context)

@login_required(login_url='client:login')
def edit(request):
    form_client = EditClientForm(request.POST or None, instance=client_instance(request.user))
    form_user = EditUserForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form_client.is_valid() and form_user.is_valid():
            form_user.save()
            form_client.save()
            messages.success(request, 'Datos actualizados correctamente')
    context = {
        'form_client': form_client,
        'form_user': form_user
    }
    return render(request, 'client/edit.html', context)

def user_filter(request):
    username = request.GET.get('username', '')
    users = User.objects.filter(username__startswith=username)
    users = [ user_serializer(user) for user in users ]
    return HttpResponse(json.dumps(users), content_type='application/json')
    # users = serializers.serialize('json', users)
    # return HttpResponse(users, content_type='application/json')

def user_serializer(user):
    return {
        'id': user.id,
        'username': user.username
    }


def client_instance(user):
    try:
        return user.client
    except:
        return Client(user = user)
    
# Class Based Views => CBV

class LoginView(View):
    form = LoginForm()
    message = None
    template = 'client/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('client:dashboard')
        return render(request, self.template, self.get_context())

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login_django(request, user) # Agrega el usuario a las variables de sesion
            return redirect(to='client:dashboard')
        else:
            self.message = 'Usuario incorrecto, verifca tus datos'
        return render(request, self.template, self.get_context())


    def get_context(self):
        context = {
            'form': self.form,
            'message': self.message
        }
        return context


class DashBoardView(LoginRequiredMixin, View):
    login_url = 'client:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'client/dashboard.html')


class ShowView(DetailView):
    model = User
    template_name = 'client/show.html'
    slug_field = 'username' # Campo de la base de datos
    #slug_url_kwarg = 'username_url'# Que atributo de la URL


class CreateUserView(CreateView):
    model = User
    template_name = 'client/create.html'
    success_url = reverse_lazy('client:login')
    form_class = CreateUserForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditUserView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = User
    login_url = reverse_lazy('client:login')
    template_name = 'client/edit.html'
    success_url = reverse_lazy('client:edit')
    form_class = EditUserForm
    success_message = 'Tu usuario ha sido actualizado'

    def get_object(self, queryset=None):
        return self.request.user

    def save(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EditUserView, self).save(request, args, kwargs)


class EditSocialNetworkView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = SocialNetwork
    login_url = 'client:login'
    template_name = 'client/edit_social.html'
    success_url = reverse_lazy('client:edit_social')
    form_class = EditClientSocialForm
    success_message = 'Datos actualizados correctament'

    def get_object(self, queryset=None):
        return self.get_social_instance()

    def get_social_instance(self):
        try:
            return self.request.user.socialnetwork
        except:
            return SocialNetwork(user=self.request.user)