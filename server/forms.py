from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    year = forms.DateField

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'year', 'name', 'first_name', 'fakultet']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fakultet': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),

        }


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text', 'link_youtube']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'details-fieldset-section'}),
            'title': forms.TextInput(attrs={'class': 'details-fieldset-section'}),
            'title': forms.TextInput(attrs={'class': 'details-fieldset-section'}),
        }


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class TeacherCreateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class ImageCreateForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Image
        fields = '__all__'


class FileCreateForm(forms.ModelForm):
    file = forms.FileField(label='File')

    class Meta:
        model = File
        fields = '__all__'
