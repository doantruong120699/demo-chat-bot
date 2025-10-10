from django.urls import path
from restaurant_booking.views import (
    restaurant_chat_stream,
    table_list,
    table_search,
    table_detail,
    booking_list,
    booking_create,
    booking_detail,
    booking_cancel,
    booking_confirm,
    booking_search_by_code
)
app_name = 'restaurant_booking'

urlpatterns = [
    # Restaurant booking chat endpoints
    path('chat/stream/', restaurant_chat_stream, name='restaurant_chat_stream'),
    
    # Table management endpoints
    path('tables/', table_list, name='table_list'),
    path('tables/search/', table_search, name='table_search'),
    path('tables/<int:table_id>/', table_detail, name='table_detail'),
    
    # Booking management endpoints
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/create/', booking_create, name='booking_create'),
    path('bookings/search/', booking_search_by_code, name='booking_search_by_code'),
    path('bookings/<int:booking_id>/', booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', booking_cancel, name='booking_cancel'),
    path('bookings/<int:booking_id>/confirm/', booking_confirm, name='booking_confirm'),
]
