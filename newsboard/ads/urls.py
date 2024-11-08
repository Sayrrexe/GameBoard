from django.urls import path
from django.contrib.auth.views import LoginView
from .views import AdDetailView
from . import views

urlpatterns = [
    # главный экран
    path('', views.index, name='index'),
    # регестрация и авторизация
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='ads/login.html'), name='login'),
    # подтвержедение почты
    path('email-confirmation/', views.email_confirmation, name='email_confirmation'),
    path('email-confirmation/resend-confirmation-code', views.resend_code_view, name='resend_confirmation_code'),
    # профиль и кнопки профиля
    path('profile/', views.profile, name='profile'),
    path('profile/toggle-subscription/', views.profile, name='toggle_subscription'),
    path('logout/', views.logout_view, name='logout'),
    path('change-newsletter-status/', views.change_newsletter, name='toggle_subscription'),
    # объявления 
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    # создание объявлений 
    path('create/', views.createView, name='create'),
    # отклик на объявление 
    path('ad/<int:ad_id>/respond/', views.submit_response, name='submit_response'),  
    # Мои отклики
    path('my-responses/', views.my_ad_responses, name='my_responses'),
]