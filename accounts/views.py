from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomRegistrationForm  # Import the new form

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Store user type in session (for later use)
            request.session['user_type'] = form.cleaned_data.get('user_type')
            
            # Success message based on user type
            user_type = form.cleaned_data.get('user_type')
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
    return render(request, 'accounts/dashboard.html', {'user': request.user})