from django.urls import path
from .views import rentacars, searched_rentacars, search_vehicles, rentacar_detail, quick_reserve, rentacar_service_reports, rate_vehicle, find_vehicles, reserve_vehicle, search_vehicles_after_reservation
urlpatterns = [
    path('', rentacars, name='rentacars'),
    path('search', searched_rentacars, name='search_rentacars'),
    path('search_vehicles', search_vehicles, name='search_vehicles'),
    path('rentacar/<int:rentacar_id>', rentacar_detail, name='rentacar_with_id'),
    path('quick_rentacar_reservation/<int:reservation_id>', quick_reserve, name='quick_reserve'),
    path('find_vehicles/<int:flight_reservation_id>', find_vehicles, name='find_vehicles'),
    path('reserve_vehicle', reserve_vehicle, name='reserve_vehicle'),
    path('search_vehicles_after_reservation', search_vehicles_after_reservation, name='search_vehicles_after_reservation'),
    path('get_rentacar_service_reports', rentacar_service_reports, name='rentacar_service_reports'),
    path('rate_vehicle', rate_vehicle, name='rate_vehicle'),
]