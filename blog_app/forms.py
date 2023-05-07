from django_quill.forms import QuillFormField
from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=50)
    body = QuillFormField()
