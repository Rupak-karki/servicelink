from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('<int:pk>/book/', views.book_service, name='book_service'),  # Added this
    path('my-bookings/', views.my_bookings, name='my_bookings'),  # Added this
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),  # Added this
    path('booking/<int:pk>/<str:status>/', views.update_booking_status, name='update_booking_status'),  # Added this
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),  # Added this
]