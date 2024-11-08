from django.contrib import admin
from .models import Ad, Category, CustomUser, Newsletter
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

admin.site.register(Category)
admin.site.register(CustomUser)


class AdAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditor5Widget())
    
    class Meta:
        model = Ad
        fields = '__all__'

class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm
    list_display = ('title', 'author', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'description')

admin.site.register(Ad, AdAdmin)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'sent')
    readonly_fields = ('created_at', 'sent')
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        
        newsletters = queryset.filter(sent=False)
        
        
        subscribers = CustomUser.objects.filter(is_subscribed=True)
        recipient_list = [subscriber.email for subscriber in subscribers]

        for newsletter in newsletters:
            try:
                send_mail(
                    subject=newsletter.title,
                    message=newsletter.content,
                    from_email=None,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                newsletter.sent = True
                newsletter.save()
                messages.success(request, f"Рассылка '{newsletter.title}' успешно отправлена.")
            except Exception as e:
                messages.error(request, f"Ошибка при отправке рассылки '{newsletter.title}': {str(e)}")
        
    send_newsletter.short_description = "Отправить выбранные рассылки"
