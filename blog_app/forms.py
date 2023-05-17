from django_quill.forms import QuillFormField
from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','blogbg','desc','timeposted']
    
    # title = forms.CharField(max_length=50)
    # blogbackground = forms.ImageField()
    # body = QuillFormField()