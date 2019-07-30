from django.urls import path, re_path
from .views import (
    CreateProjecView, 
    ListProjectsView,
    ListMyProjectsView,
    DetailProjectView,
    ListContributorsView,
    edit,
    add_contributor,
    delete_contributor,
    user_contributor
)


app_name = 'project'

urlpatterns = [
    path('', ListProjectsView.as_view(), name='projects'),
    path('mine/', ListMyProjectsView.as_view(), name='my_projects'),
    path('create/', CreateProjecView.as_view(), name='create'),
    path('<slug:slug>/', DetailProjectView.as_view(), name='show'),
    path('<slug:slug>/edit/', edit, name='edit'),
    path('<slug:slug>/contributors/', ListContributorsView.as_view(), name='contributors'),
    path('<slug:slug>/contributors/add/<username>/', add_contributor, name='add_contributor'),
    path('<slug:slug>/contributors/delete/<username>/', delete_contributor, name='delete_contributor'),
    path('<slug:slug>/contributors/<username>/', user_contributor, name='user_contributor'),
]