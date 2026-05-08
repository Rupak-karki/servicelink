from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('my-services/', views.provider_services, name='provider_services'),
    path('add-service/', views.add_service, name='add_service'),
    
    # Booking URLs (specific patterns first)
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:pk>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    
    # Review URLs
    path('review/<int:booking_id>/', views.leave_review, name='leave_review'),
    
    # Service URLs (these have <int:pk> so put them last)
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete_service'),
    path('<int:pk>/book/', views.book_service, name='book_service'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
]