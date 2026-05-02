from django.shortcuts import render, get_object_or_404
from .models import Service, Category

def service_list(request):
    services = Service.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Handle search
    query = request.GET.get('q')
    if query:
        services = services.filter(title__icontains=query)
    
    # Handle category filter
    category_slug = request.GET.get('category')
    if category_slug:
        services = services.filter(category__slug=category_slug)
    
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/service_list.html', context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_available=True)
    return render(request, 'services/service_detail.html', {'service': service})