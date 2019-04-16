from django.urls import path
from .views import airlines, search_airlines, search_flights, flight_detail
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='airlines_home.html'), name='airlines'),
    path('search_flights', search_flights, name='search_flights'),
    path('search_airlines', search_airlines, name='search_airlines'),
    path('flight/<int:flight_id>', flight_detail, name='flight_with_id'),
]