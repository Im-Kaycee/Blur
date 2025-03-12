from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from .forms import SignupForm, LoginForm, UserCreationForm
from django.contrib.auth import logout
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

class user_register(generic.CreateView):
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('user_login')  

def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('user_login')  