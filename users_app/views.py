from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            messages.success(request, f'Your account has been created successfully. Now you can login!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    context = { 'form': form}
    return render(request, 'users_app/register.html', context)


@login_required
def profile(request):
    return render(request, 'users_app/profile.html')
