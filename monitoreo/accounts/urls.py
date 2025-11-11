# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Auth & Profile
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('profile/', views.profile_view, name='profile'), # <-- Esta es la vista que creamos
]