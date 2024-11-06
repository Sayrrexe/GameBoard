from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.index, name='login'),
    path('email-confirmation/', views.email_confirmation, name='email_confirmation'),
    path('profile/', views.profile, name='profile'),
    path('profile/toggle-subscription/', views.profile, name='toggle_subscription'),
    path('logout/', views.logout_view, name='logout'),
    path('change-newsletter-status/', views.change_newsletter, name='toggle_subscription')
]
