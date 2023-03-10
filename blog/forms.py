from django import forms
from .models import *
#from django.core.exceptions import ValidationError
#from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','author']

    #def clean_name(self):
    #    """Make sure people don't use my name"""
    #    data = self.cleaned_data['name']
    #    if not self.request.user.is_authenticated and data.lower().strip() == 'samuel':
    #        raise ValidationError("Sorry, you cannot use this name.")
    #    return data
    

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('updated_on','created_on', 'is_active','view_count','tags')



#class CommentForm(forms.ModelForm):
#
#    class Meta:
#        model = Comment
#        fields = {'content','author', 'authorEmail'}