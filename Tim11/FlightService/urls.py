from django.urls import path
from .views import *
from django.views.generic import TemplateView
urlpatterns = [
    path('', airlines, name='airlines'),
    path('search_flights', search_flights, name='search_flights'),
    path('search_airlines', search_airlines, name='search_airlines'),
    path('flight/<int:flight_id>', flight_detail, name='flight_with_id'),
    path('airline/<int:airline_id>', airline_detail, name='airline_with_id'),
    path('reservation/<int:reservation_id>', reserve, name='reserve_flight'),
    path('get_flight_service_reports', flight_service_reports, name='flight_service_reports'),
    path('rate_flight', rate_flight, name='rate_flight'),
    path('finish_flight_reservation', finish_flight_reservation),
    path('invite/<int:reservation_id>', invite),
    path('cancel_invite/<int:reservation_id>', cancel_invite, name='cancel_invite'),
    path('accept_invite/<int:reservation_id>', accept_invite, name='accept_invite'),
    path('get_rating_airline', get_rating_airline, name='get_rating_airline')

]