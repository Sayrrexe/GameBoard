from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Ad

class AdForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    
    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'status']