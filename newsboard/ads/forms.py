from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Ad

class AdForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'status']