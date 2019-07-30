from django.urls import path, re_path
from . import views

app_name = 'client'

urlpatterns = [
    path('show/<slug:slug>', views.ShowView.as_view(), name='show'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('edit/', views.edit, name='edit'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('edit/social/', views.EditSocialNetworkView.as_view(), name='edit_social'),
    re_path('filter$', views.user_filter, name='filter'),
]