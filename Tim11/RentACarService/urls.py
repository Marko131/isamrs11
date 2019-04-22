from django.urls import path
from .views import rentacars, searched_rentacars, search_vehicles, rentacar_detail
urlpatterns = [
    path('', rentacars, name='rentacars'),
    path('search', searched_rentacars, name='search_rentacars'),
    path('search_vehicles', search_vehicles, name='search_vehicles'),
    path('rentacar/<int:rentacar_id>', rentacar_detail, name='rentacar_with_id'),
]