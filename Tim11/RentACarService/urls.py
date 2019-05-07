from django.urls import path
from .views import rentacars, searched_rentacars, search_vehicles, rentacar_detail, reserve, rentacar_service_reports, rate_vehicle
urlpatterns = [
    path('', rentacars, name='rentacars'),
    path('search', searched_rentacars, name='search_rentacars'),
    path('search_vehicles', search_vehicles, name='search_vehicles'),
    path('rentacar/<int:rentacar_id>', rentacar_detail, name='rentacar_with_id'),
    path('rentacar_reservation/<int:reservation_id>', reserve, name='reserve'),
    path('get_rentacar_service_reports', rentacar_service_reports, name='rentacar_service_reports'),
    path('rate_vehicle', rate_vehicle, name='rate_vehicle'),
]