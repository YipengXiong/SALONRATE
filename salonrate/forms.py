from django import forms
from django.contrib.auth.models import User
from salonrate.models import UserProfile, Comment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'star', 'tag_environ', 'tag_service', 'tag_cost', 'tag_skill', 'tag_attitude', )