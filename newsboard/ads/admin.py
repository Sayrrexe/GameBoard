from django.contrib import admin
from .models import Ad, Category, CustomUser

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(CustomUser)