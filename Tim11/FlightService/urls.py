from django.urls import path
from .views import airlines, searched_airlines
urlpatterns = [
    path('', airlines, name='airlines'),
    path('search', searched_airlines, name='search')
]