from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resume, Company, Vacancy
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['phone', 'profile_pic']


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'salary', 'status', 'specialty', 'grade', 'education', 'experience',
                  'portfolio']
        # exclude = ['user', 'profile_pic']


class MyCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'location', 'description', 'employee_count']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['published_at','company', 'published_at']


