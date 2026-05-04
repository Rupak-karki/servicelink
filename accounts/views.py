from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomRegistrationForm  # Import the new form
from .models import UserProfile  # Added this import


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

             # Update the user profile with the selected user type
            user_type = form.cleaned_data.get('user_type')
            profile = user.profile
            profile.user_type = user_type
            profile.phone = form.cleaned_data.get('phone', '')
            profile.save()
            
            login(request, user)
            
            # Success message based on user type
            if user_type == 'provider':
                messages.success(request, f'Welcome {user.username}! You registered as a Service Provider. Please complete your business profile.')
            else:
                messages.success(request, f'Welcome {user.username}! Registration successful. Start exploring services!')
            
            return redirect('dashboard')
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})          




@login_required
def dashboard(request):
    # Get user type from database, not session
    user_type = request.user.profile.user_type
    return render(request, 'accounts/dashboard.html', {
        'user': request.user,
        'user_type': user_type
    })