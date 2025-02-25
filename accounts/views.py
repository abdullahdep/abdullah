from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm, ChildAccountForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

def index(request):
    return render(request, 'accounts/index.html')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def create_child_account(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        child_form = ChildAccountForm(request.POST)
        if form.is_valid() and child_form.is_valid():
            user = form.save()
            child_profile = child_form.save(commit=False)
            child_profile.user = user
            child_profile.is_child_account = True
            child_profile.parent_account = request.user
            child_profile.save()
            messages.success(request, f'Child account created for {user.username}!')
            return redirect('home')
    else:
        form = SignUpForm()
        child_form = ChildAccountForm()
    return render(request, 'accounts/create_child_account.html', {'form': form, 'child_form': child_form})

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'

