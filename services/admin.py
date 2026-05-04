from django.contrib import admin
from .models import Category, Service, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'provider', 'is_available']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['title', 'description']

#  new admin for Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'service', 'booking_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']  # Change status directly in list view
    search_fields = ['customer__username', 'service__title']
    date_hierarchy = 'booking_date'