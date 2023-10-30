from django import forms
from .models import Announcement, Response
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['categories', 'name', 'text']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']