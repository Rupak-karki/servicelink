from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Service, Category

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