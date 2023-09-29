from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class NewForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['categories', 'header', 'text']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
