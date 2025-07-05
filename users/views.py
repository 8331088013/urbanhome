from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm
from listings.models import Property, Favorite, Message
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to UrbanHome.')
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homefinder:home')

@login_required
def dashboard(request):
    # Get user's properties
    user_properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    
    # Get user's favorites
    user_favorites = Favorite.objects.filter(user=request.user).select_related('property').order_by('-created_at')
    
    # Get received messages
    received_messages = Message.objects.filter(receiver=request.user).select_related('sender', 'property').order_by('-created_at')
    
    # Calculate total views (placeholder for now)
    total_views = 0
    
    context = {
        'user_properties': user_properties,
        'user_favorites': user_favorites,
        'received_messages': received_messages,
        'total_views': total_views,
    }
    
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

# Create your views here.
