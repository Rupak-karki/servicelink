from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count, Avg, Sum  # Added these imports
from services.models import Booking, Review  # Added this import
from .forms import (
    CustomRegistrationForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import UserProfile


def register(request):
    """User registration with role and profile setup"""
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Update the user profile with the selected user type and phone
            user_type = form.cleaned_data.get('user_type')
            profile = user.profile
            profile.user_type = user_type
            profile.phone = form.cleaned_data.get('phone', '')
            profile.save()

            login(request, user)

            # Success message based on user type
            if user_type == 'provider':
                messages.success(
                    request,
                    f'Welcome {user.username}! You registered as a Service Provider. '
                    'Please complete your business profile.'
                )
            else:
                messages.success(
                    request,
                    f'Welcome {user.username}! Registration successful. Start exploring services!'
                )

            return redirect('dashboard')
    else:
        form = CustomRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard view"""
    user_type = request.user.profile.user_type
    return render(request, 'accounts/dashboard.html', {
        'user': request.user,
        'user_type': user_type,
    })


@login_required
def profile_view(request):
    """View user profile with statistics"""
    user = request.user
    profile = user.profile
    
    # Initialize statistics
    stats = {
        'services_count': 0,
        'bookings_count': 0,
        'reviews_count': 0,
        'total_earnings': 0,
        'avg_rating': 0
    }
    
    if profile.user_type == 'provider':
        # Count provider's services
        stats['services_count'] = user.services.count()
        
        # Count bookings for provider's services
        stats['bookings_count'] = Booking.objects.filter(
            service__provider=user
        ).count()
        
        # Count completed bookings for earnings
        completed_bookings = Booking.objects.filter(
            service__provider=user,
            status='completed'
        )
        stats['completed_bookings'] = completed_bookings.count()
        
        # Calculate total earnings (sum of service prices for completed bookings)
        total_earnings = 0
        for booking in completed_bookings:
            total_earnings += booking.service.price
        stats['total_earnings'] = total_earnings
        
        # Calculate average rating
        reviews = Review.objects.filter(booking__service__provider=user)
        stats['reviews_count'] = reviews.count()
        if reviews.exists():
            avg = reviews.aggregate(Avg('rating'))['rating__avg']
            stats['avg_rating'] = round(avg, 1)
    
    elif profile.user_type == 'customer':
        # Count customer's bookings
        stats['bookings_count'] = Booking.objects.filter(customer=user).count()
        
        # Count customer's reviews
        stats['reviews_count'] = Review.objects.filter(booking__customer=user).count()
    
    return render(request, 'accounts/profile_view.html', {
        'user': user,
        'profile': profile,
        'stats': stats
    })


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_type': request.user.profile.user_type,
    })


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
