from django.conf import settings
from django.views.generic import DetailView
from django.db.models import Q


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .utils import create_confirmation_code
from .forms import AdForm, ResponseForm
from .models import Ad, Category, CustomUser, Response, ConfirmationCode


from django.db.models import Q

# Главная страница с объявлениями
def index(request):
    category_name = request.GET.get('category')
    search_query = request.GET.get('q')
    
    # Начальная фильтрация объявлений по статусу "опубликовано"
    ads = Ad.objects.filter(status='published')

    # Фильтрация по категории, если указана
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            ads = ads.filter(category=category)
        except Category.DoesNotExist:
            ads = Ad.objects.none()  
    
    # Фильтрация по поисковому запросу, если он указан
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    categories = Category.objects.all()
    return render(request, 'ads/index.html', {'ads': ads, 'categories': categories})



# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        usernamecheck = username.lower()
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Проверка уникальности имени пользователя и email
        if CustomUser.objects.filter(username__iexact=usernamecheck).exists():
            messages.error(request, "Имя пользователя уже занято")
            return render(request, 'ads/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Данная почта уже занята!")
            return render(request, 'ads/register.html')
        
        # Проверка совпадения паролей
        if password != confirm_password:
            messages.error(request, "Пароли не совпадают")
            return render(request, 'ads/register.html')
        
        # Создание пользователя и вход в систему
        
        
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, is_active = False)
        except Exception as e:
            messages.error(request, f"Ошибка при создании пользователя: {str(e)}")
            return render(request, 'ads/register.html')
        
        login(request, user)
        confirmation_code = create_confirmation_code(user)
        
        return redirect('email_confirmation')
    
    return render(request, 'ads/register.html')

# Подтверждение email пользователя
def email_confirmation(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.user
        
        try:
            confirmation = ConfirmationCode.objects.get(user=user, code=code)
            if confirmation.is_active():
                if confirmation.code == code:
                    user.is_email_verified = True
                    user.is_active = True
                    user.save()
                    confirmation.delete()
                    messages.success(request, "Email успешно подтверждён!")
                    return redirect('index')
            else:
                messages.error(request, "Код подтверждения истёк. Запросите новый.")
                confirmation.delete()  
        except ConfirmationCode.DoesNotExist:
            messages.error(request, "Неправильный код подтверждения")
    
    return render(request, 'ads/email_confirmation.html')


# Профиль пользователя
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        if 'first_name' in request.POST:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            messages.success(request, "Профиль обновлён")
            return redirect('profile')
    return render(request, 'ads/profile.html')

# Выход из аккаунта
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта")
    return redirect('index')  

# Управление подпиской на рассылку
def change_newsletter(request):
    user = request.user
    user.is_subscribed = not user.is_subscribed
    user.save()
    if user.is_subscribed:
        messages.success(request, "Вы подписались на рассылку")
    else:
        messages.info(request, "Вы отписались от рассылки")
    return redirect('profile')


# Детализация объявления
class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResponseForm()
        return context

# Создание и редактирование объявления
@login_required
def createView(request):
    ad_id = request.GET.get('edit')
    ad_to_edit = None

    if ad_id:
        ad_to_edit = get_object_or_404(Ad, id=ad_id, author=request.user)
        form = AdForm(request.POST or None, request.FILES or None, instance=ad_to_edit)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AdForm(request.POST or None, request.FILES or None)
        if request.method == 'POST' and form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, "Вы успешно добавили новость!")
            return redirect('index')

    ads = Ad.objects.filter(author=request.user)
    context = {
        'form': form,
        'ads': ads,
        'ad_to_edit': ad_to_edit,
    }
    return render(request, 'ads/myads.html', context)

# Отклик на объявление
@login_required
def submit_response(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, status='published')
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.sender = request.user
            response.status = 'pending'
            response.save()
            try:
                send_mail(
                    subject='Новый отклик на ваше объявление',
                    message=f'Пользователь {request.user.username} оставил отклик на ваше объявление "{ad.title}".\n\nТекст отклика:\n{response.content}',
                    from_email=None,
                    recipient_list=[ad.author.email],
                    fail_silently=False,
                    
                )
                messages.success(request, "Ваш отклик успешно отправлен!")
            except Exception as e:
                messages.error(request, "Не удалось отправить email. Попробуйте позже.")
            return redirect('ad_detail', pk=ad.id)
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ResponseForm()
    
    return render(request, 'ads/submit_response.html', {'form': form, 'ad': ad})

# Повторная отправка кода подтверждения email
@login_required
def resend_code_view(request):
    user = request.user
    confirmation_code = create_confirmation_code(user)
    messages.info(request, 'Код отправлен на вашу почту')
    return redirect('email_confirmation')

# Удаление и принятие откликов на объявления пользователя
@login_required
def my_ad_responses(request):
    user_ads = Ad.objects.filter(author=request.user)
    ad_id = request.GET.get('ad_id')  # Для фильтрации по конкретному объявлению

    if ad_id:
        responses = Response.objects.filter(ad__id=ad_id, ad__author=request.user)
    else:
        responses = Response.objects.filter(ad__in=user_ads)

    if request.method == 'POST' and 'delete_response' in request.POST:
        response_id = request.POST.get('delete_response')
        response_to_delete = get_object_or_404(Response, id=response_id, ad__author=request.user)
        response_to_delete.delete()
        messages.success(request, "Отклик успешно удалён.")
        return redirect('my_responses')

    if request.method == 'POST' and 'accept_response' in request.POST:
        response_id = request.POST.get('accept_response')
        response_to_accept = get_object_or_404(Response, id=response_id, ad__author=request.user)
        response_to_accept.status = 'accepted'
        response_to_accept.save()
        
        send_mail(
            subject='Ваш отклик был принят',
            message=f'Ваш отклик на объявление "{response_to_accept.ad.title}" был принят.',
            from_email=None,
            recipient_list=[response_to_accept.sender.email],
            fail_silently=False,
        )
    
        messages.success(request, "Отклик успешно принят и уведомление отправлено.")
        return redirect('my_responses')

    context = {
        'user_ads': user_ads,
        'responses': responses,
    }
    return render(request, 'ads/my_responses.html', context)

