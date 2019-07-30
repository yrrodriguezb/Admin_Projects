from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from status.forms import StatusChoicesForm
from status.models import Status
from .forms import ProjectCreateForm, PermissionProjectForm
from .models import Project, ProjectUser, ProjectPermission


""" Funcion decoradora para validar permisos """
def admin_only(function):
    def wrap(request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])

        if not project.user_has_permission(request.user):
            lazy = reverse_lazy('project:show', kwargs={ 'slug': project.slug })
            return HttpResponseRedirect(lazy)

        return function(request, *args, **kwargs)
    return wrap

@login_required(login_url='client:login')
@admin_only
def edit(request, slug=''):
    project = get_object_or_404(Project, slug=slug)
    form_project = ProjectCreateForm(request.POST or None, instance=project)
    form_status = StatusChoicesForm(request.POST or None, initial = {
        'status': project.get_status_id()
    } )

    if request.method == 'POST':
        if form_status.is_valid() and form_project.is_valid():
            selection_status_id = form_status.cleaned_data['status'].id
            form_project.save()

            if selection_status_id != project.get_status_id():
                project.projectstatus_set.create(status_id=selection_status_id)
                
            messages.success(request, 'Los datos se actualizaron correctamente')

    context = { 
        'form_project': form_project,
        'form_status': form_status
    }
    return render(request, 'project/edit.html', context)

@login_required(login_url='client:login')
@admin_only
def add_contributor(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=username)

    if not project.projectuser_set.filter(user=user).exists():
        project.projectuser_set.create(
            user=user, 
            permission=ProjectPermission.contributor_permission())

    return redirect('project:contributors', slug=project.slug)


@login_required(login_url='client:login')
def user_contributor(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=username)
    has_permission = project.user_has_permission(request.user)
    permission = get_object_or_404(ProjectUser, user=user, project=project)
    form = PermissionProjectForm(
        request.POST or None,
        initial={ 'permission': permission.permission_id }
    )

    if request.method == 'POST' and form.is_valid():
        selection_id = form.cleaned_data['permission'].id
        if selection_id != permission.id and permission.valid_change_permission():
            permission.permission_id = selection_id
            permission.save()
            messages.success(request, 'Datos actualizados correctamente')

    context = {
        'project': project,
        'user': user,
        'has_permission': has_permission,
        'form': form
    }

    return render(request, 'project/contributor.html',context)

@login_required(login_url='client:login')
@admin_only
def delete_contributor(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=username)
    project_user = get_object_or_404(ProjectUser, user=user, project=project)
    if not project_user.is_founder():
        project_user.delete()

    return redirect('project:contributors', slug=project.slug)

class CreateProjecView(LoginRequiredMixin, CreateView):
    model = Project
    login_url = 'client:login'
    template_name = 'project/create.html'
    form_class = ProjectCreateForm

    # Rollback
    @transaction.atomic
    def create_objects(self):
        self.object.save()
        self.object.projectstatus_set.create(status=Status.get_default_status())
        self.object.projectuser_set.create(
            user=self.request.user, 
            permission=ProjectPermission.founder_permission())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.create_objects()
        return HttpResponseRedirect(self.get_url_project())

    def get_url_project(self):
        return reverse_lazy('project:show', kwargs={ 'slug': self.object.slug })

class ListProjectsView(LoginRequiredMixin,  ListView):
    model = Project
    login_url = 'client:login'
    template_name = 'project/index.html'

    def get_queryset(self):
        return Project.objects.all()

class ListMyProjectsView(LoginRequiredMixin,  ListView):
    model = Project
    login_url = 'client:login'
    template_name = 'project/mine.html'

    def get_queryset(self):
        return ProjectUser.objects.filter(user=self.request.user)

class DetailProjectView(DetailView):
    model = Project
    template_name = 'project/show.html'

    def get_context_data(self, **kwargs):
        context = super(DetailProjectView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context['has_permission'] = self.object.user_has_permission(self.request.user)
        return context

class ListContributorsView(ListView):
    model = Project
    template_name = 'project/contributors.html'

    def get_queryset(self):
        self.project = get_object_or_404(Project, slug=self.kwargs['slug'])
        return ProjectUser.objects.filter(project=self.project)

    """ 
        self.project, se obtiene ya que get_queryset se ejecuta antes 
        de get_context_data
    """
    def get_context_data(self, **kwargs):
        context = super(ListContributorsView, self).get_context_data(**kwargs)
        context["project"] = self.project
        return context
    

    

    

    

