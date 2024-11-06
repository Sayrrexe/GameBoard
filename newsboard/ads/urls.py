from django.urls import path
from django.contrib.auth.views import LoginView
from .views import AdDetailView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('email-confirmation/', views.email_confirmation, name='email_confirmation'),
    path('profile/', views.profile, name='profile'),
    path('profile/toggle-subscription/', views.profile, name='toggle_subscription'),
    path('logout/', views.logout_view, name='logout'),
    path('change-newsletter-status/', views.change_newsletter, name='toggle_subscription'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
]
