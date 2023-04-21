from django import forms
from .models import User, FAQ


class AboutForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['id', 'about_me']

class TestimonialForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['id', 'testimonial']

class UserMainImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone','main_image']