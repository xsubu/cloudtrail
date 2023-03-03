from django import forms
from .models import *


class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('updated_on','created_on', 'is_active','view_count','tags')