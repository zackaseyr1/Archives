from django import forms
from .models import Project, Folder
from tinymce.widgets import TinyMCE
from store.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'department')

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'department')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'department', 'block']



class ProjectForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'richtext'}))
    class Meta:
        model = Project
        fields = ['department', 'title', 'description']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['title', 'description', 'folder']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'folder': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)