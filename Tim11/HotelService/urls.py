from django.urls import path
from .views import hotels, searched_hotels
urlpatterns = [
    path('', hotels, name='hotels'),
    path('search', searched_hotels, name='search_hotels')
]