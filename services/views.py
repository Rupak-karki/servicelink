from django.shortcuts import render, get_object_or_404, redirect  # Added 'redirect'
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # Added this
from django.contrib import messages  # Added this
from .models import Service, Category, Booking  # Added 'Booking'
from .forms import BookingForm  # Added this

from .forms import ServiceForm


def service_list(request):
    # Start with all available services
    services = Service.objects.filter(is_available=True)
    
    # Get filter parameters from URL
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', '-created_at')  # Default: newest first
    
    # === SEARCH FILTER ===
    if query:
        services = services.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    # === CATEGORY FILTER ===
    if category_slug:
        services = services.filter(category__slug=category_slug)
    
    # === PRICE FILTER ===
    if min_price:
        services = services.filter(price__gte=min_price)  # greater than or equal
    if max_price:
        services = services.filter(price__lte=max_price)  # less than or equal
    
    # === SORTING ===
    valid_sorts = ['price', '-price', 'created_at', '-created_at', 'title']
    if sort_by in valid_sorts:
        services = services.order_by(sort_by)
    
    # === PAGINATION (6 items per page) ===
    paginator = Paginator(services, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'services': page_obj,  # Paginated services
        'categories': categories,
        'search_query': query,
        'selected_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'services/service_list.html', context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_available=True)
    
    # Get related services (same category, exclude current)
    related_services = Service.objects.filter(
        category=service.category, 
        is_available=True
    ).exclude(pk=pk)[:3]  # Show max 3 related services
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'services/service_detail.html', context)

# for booking system


# Add this view - Book a service
@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk, is_available=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.customer = request.user
            booking.save()
            messages.success(request, f'Your booking for "{service.title}" has been submitted! Provider will confirm soon.')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'services/book_service.html', {
        'form': form,
        'service': service
    })

# Add this view - My Bookings (Customer view)
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'services/my_bookings.html', {
        'bookings': bookings
    })

# Add this view - Manage Bookings (Provider view)
@login_required
def manage_bookings(request):
    # Get all bookings for services that this user provides
    # Only providers can access

    if request.user.profile.user_type != 'provider':
        messages.error(request, 'Access denied. Provider only area.')
        return redirect('dashboard')

    bookings = Booking.objects.filter(service__provider=request.user)
    return render(request, 'services/manage_bookings.html', {
        'bookings': bookings
    })

# Add this view - Update booking status
@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk, service__provider=request.user)
    
    valid_statuses = ['confirmed', 'completed', 'cancelled']
    if status in valid_statuses:
        booking.status = status
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been {status}!')
    
    return redirect('manage_bookings')

# Add this view - Cancel booking (Customer)
@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'Cannot cancel booking at this stage.')
    
    return redirect('my_bookings')


@login_required
def provider_services(request):
    # Only providers can access
    if request.user.profile.user_type != 'provider':
        messages.error(request, 'Access denied. Provider area only.')
        return redirect('dashboard')
    
    services = Service.objects.filter(provider=request.user)
    return render(request, 'services/provider_services.html', {'services': services})


@login_required
def add_service(request):
    """Provider can add a new service"""
    if request.user.profile.user_type != 'provider':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, f'Service "{service.title}" has been added successfully!')
            return redirect('provider_services')
    else:
        form = ServiceForm()
    
    return render(request, 'services/add_service.html', {'form': form})

@login_required
def edit_service(request, pk):
    """Provider can edit their service"""
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{service.title}" has been updated!')
            return redirect('provider_services')
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'services/edit_service.html', {'form': form, 'service': service})

@login_required
def delete_service(request, pk):
    """Provider can delete their service"""
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    
    if request.method == 'POST':
        service_title = service.title
        service.delete()
        messages.success(request, f'Service "{service_title}" has been deleted.')
        return redirect('provider_services')
    
    return render(request, 'services/delete_service.html', {'service': service})