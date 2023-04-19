from django import forms
from .models import User, FAQ


class FAQForm(forms.ModelForm):
  
    class Meta:
        model = FAQ
        fields = ['id', 'body']