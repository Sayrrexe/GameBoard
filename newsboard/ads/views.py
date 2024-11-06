from django.shortcuts import render
from .models import Ad, Category

def index(request):
    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            ads = Ad.objects.filter(category=category)
        except Category.DoesNotExist:
            ads = Ad.objects.none()  # Если категории нет, не показывать объявления
    else:
        ads = Ad.objects.all()
    categories = Category.objects.all()
    return render(request, 'ads/index.html', {'ads': ads, 'categories': categories})
