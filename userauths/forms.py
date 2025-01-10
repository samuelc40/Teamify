from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your First Name', 'class': 'input field input-field'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your last Name', 'class': 'input field input-field'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'input field input-field'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email', 'class': 'input field input-field'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'input field input-field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'input field input-field'}))

    class Meta:
        
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password1', 'password2']