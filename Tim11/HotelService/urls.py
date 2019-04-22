from django.urls import path
from .views import hotels, searched_hotels, search_rooms, hotel_detail
urlpatterns = [
    path('', hotels, name='hotels'),
    path('search', searched_hotels, name='search_hotels'),
    path('search_rooms', search_rooms, name='search_rooms'),
    path('hotel/<int:hotel_id>', hotel_detail, name='hotel_with_id'),
]