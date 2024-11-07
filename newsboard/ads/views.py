from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import AdForm
from .models import Ad, Category, CustomUser

def index(request):
    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            ads = Ad.objects.filter(category=category, status='published')
        except Category.DoesNotExist:
            ads = Ad.objects.none()  # Если категории нет, не показывать объявления
    else:
        ads = Ad.objects.filter(status='published')
    categories = Category.objects.all()
    return render(request, 'ads/index.html', {'ads': ads, 'categories': categories})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        usernamecheck = username.lower()
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Проверка на уникальность username
        if CustomUser.objects.filter(username__iexact=usernamecheck).exists():
            messages.error(request, "Имя пользователя уже занято")
            return render(request, 'ads/register.html')

        if CustomUser.objects.filter(email = email).exists():
            messages.error(request, "Данная почта уже занята!")
            return render(request, 'ads/register.html')
        
        if password != confirm_password:
            messages.error(request, "Пароли не совпадают")
            return render(request, 'ads/register.html')
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Регистрация успешна! Вы вошли в систему.")
        return redirect('email_confirmation')
    
    return render(request, 'ads/register.html')



def email_confirmation(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        
        # Проверка кода
        if code == "123456":
            user = request.user
            user.is_email_verified = True
            user.save()
            messages.success(request, "Email успешно подтверждён!")
            return redirect('index')
        else:
            messages.error(request, "Неправильный код подтверждения")
    return render(request, 'ads/email_confirmation.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('register')
    user = request.user

    if request.method == 'POST':
        if 'first_name' in request.POST:
            # Обработка формы для редактирования профиля
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            messages.success(request, "Профиль обновлён")
            return render(request, 'ads/profile.html')
    return render(request, 'ads/profile.html')


def logout_view(request):
        logout(request)
        messages.info(request, "Вы вышли из аккаунта")
        
        return redirect('index')  # Перенаправляем на главную страницу
    
def change_newsletter(request):
    user = request.user
    user.is_subscribed = not user.is_subscribed
    user.save()
    if user.is_subscribed:
        messages.success(request, "Вы подписались на рассылку")
    else:
        messages.info(request, "Вы отписались от рассылки")
    return redirect('profile')  

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'  # Шаблон для страницы объявления
    context_object_name = 'ad'
    
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
            return redirect('index')

    ads = Ad.objects.filter(author=request.user)
    context = {
        'form': form,
        'ads': ads,
        'ad_to_edit': ad_to_edit,
    }
    return render(request, 'ads/myads.html', context)
