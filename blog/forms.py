from django import forms
from .models import *
#from django.core.exceptions import ValidationError
#from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','author']
        widget = {
            'author': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }

    #def clean_name(self):
    #    """Make sure people don't use my name"""
    #    data = self.cleaned_data['name']
    #    if not self.request.user.is_authenticated and data.lower().strip() == 'samuel':
    #        raise ValidationError("Sorry, you cannot use this name.")
    #    return data
    

class CustomMMCF(forms.ModelMultipleChoiceField):

    def label_from_instance(self, member):
        return '%s' % member.name

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('updated_on','created_on', 'is_active','view_count')

        headline = forms.CharField()
    
        tags = CustomMMCF(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )
        #tags = forms.ModelMultipleChoiceField(
        #queryset=Tag.objects.all(),
        #widget=forms.CheckboxSelectMultiple
        #)



#class CommentForm(forms.ModelForm):
#
#    class Meta:
#        model = Comment
#        fields = {'content','author', 'authorEmail'}