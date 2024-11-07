from django.contrib import admin
from .models import Ad, Category, CustomUser
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.register(Category)
admin.site.register(CustomUser)



class AdAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Ad
        fields = '__all__'

class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm
    list_display = ('title', 'author', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'description')

admin.site.register(Ad, AdAdmin)
