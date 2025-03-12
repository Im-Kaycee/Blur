from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 rounded border border-slate-600 bg-slate-700 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full py-2 rounded border border-slate-600 bg-slate-700 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Password',
        })
    )

class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 rounded border border-slate-600 bg-slate-700 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full py-2 rounded border border-slate-600 bg-slate-700 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Email',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full py-2 rounded border border-slate-600 bg-slate-700 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full py-2 rounded border border-slate-600 bg-slate-700 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']  # Ensure email gets saved
            if commit:
                user.save()
            return user