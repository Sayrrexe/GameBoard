from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_subscribed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        try:
            # Получаем старый аватар из базы данных
            old_avatar = CustomUser.objects.get(pk=self.pk).avatar
        except CustomUser.DoesNotExist:
            old_avatar = None

        # Удаляем старый файл, если он существует и новый файл загружен
        if old_avatar and self.avatar != old_avatar:
            old_avatar.delete(save=False)

        # Сохраняем новый аватар
        super(CustomUser, self).save(*args, **kwargs)

