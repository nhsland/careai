from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Developer, Clinician, Profile


class DeveloperRegisterForm(UserCreationForm):
    email = forms.EmailField() # required in order to make it a compulsory field

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # included to make email appear before passwords (more intuitive)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)  # commit set to False to return object not saved to db yet
        user.is_developer = True
        user.save()
        Developer.objects.create(user=user)  # creates developer based on user instance
        return user


class ClinicianRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_clinician = True
        user.is_active = False
        if commit:
            user.save()
        Clinician.objects.create(user=user)
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
