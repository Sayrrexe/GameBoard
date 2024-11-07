from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django_ckeditor_5.fields import CKEditor5Field


class CustomUser(AbstractUser):
    info = models.TextField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_subscribed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        
        old_avatar = None
        if self.pk:
            try:
                old_avatar = CustomUser.objects.get(pk=self.pk).avatar
            except CustomUser.DoesNotExist:
                pass
        
        
        if self.avatar:
            ext = os.path.splitext(self.avatar.name)[1]  
            self.avatar.name = f'avatar_{self.pk}{ext}'
        
        
        if old_avatar and old_avatar != self.avatar:
            old_avatar.delete(save=False)

        super(CustomUser, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Content', config_name='default')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[('published', 'Опубликовано'), ('draft', 'Черновик')])
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        
    
        

    
class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Ожидает'), ('accepted', 'Принят'), ('rejected', 'Отклонён')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.sender
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_date = models.DateTimeField(null=False)
    sent = models.BooleanField(default=False)

