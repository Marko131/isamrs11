from django.urls import path
from .views import airlines, search_airlines, search_flights, flight_detail, airline_detail, reserve, flight_service_reports
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='airlines_home.html'), name='airlines'),
    path('search_flights', search_flights, name='search_flights'),
    path('search_airlines', search_airlines, name='search_airlines'),
    path('flight/<int:flight_id>', flight_detail, name='flight_with_id'),
    path('airline/<int:airline_id>', airline_detail, name='airline_with_id'),
    path('reservation/<int:reservation_id>', reserve, name='reserve'),
    path('get_flight_service_reports', flight_service_reports, name='flight_service_reports')
]