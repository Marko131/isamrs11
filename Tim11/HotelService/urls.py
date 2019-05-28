from django.urls import path
from .views import hotels, searched_hotels, search_rooms, hotel_detail, find_rooms, reserve_room, search_rooms_after_reservation, reserve_quick_room, rate_room, hotel_service_reports
urlpatterns = [
    path('', hotels, name='hotels'),
    path('search', searched_hotels, name='search_hotels'),
    path('search_rooms', search_rooms, name='search_rooms'),
    path('hotel/<int:hotel_id>', hotel_detail, name='hotel_with_id'),

    path('find_rooms/<int:flight_reservation_id>/<int:passengers>', find_rooms, name='find_rooms'),
    path('reserve_room', reserve_room, name='reserve-room'),
    path('search_rooms_after_reservation', search_rooms_after_reservation, name='search_rooms_after_reservation'),
    path('reserve_quick_room', reserve_quick_room, name='reserve_quick_room'),
    path('rate_room', rate_room, name='rate_room'),
    path('get_hotel_service_reports', hotel_service_reports, name='hotel_service_reports'),
]