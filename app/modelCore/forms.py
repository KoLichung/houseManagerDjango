from django import forms
from .models import User, FAQ



class UserAvatarForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['id','avatar']


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
        fields = ['id','main_image']
