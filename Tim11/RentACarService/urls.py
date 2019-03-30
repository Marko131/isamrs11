from django.urls import path
from .views import rentacars, searched_rentacars
urlpatterns = [
    path('', rentacars, name='rentacars'),
    path('search', searched_rentacars, name='search_rentacars')
]