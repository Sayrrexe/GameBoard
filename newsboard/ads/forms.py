from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Ad, Response

class AdForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    
    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'status']
        
        
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Введите ваш отклик здесь...',
                'required': True,
            }),
        }
        labels = {
            'content': 'Ваш отклик',
        }