from django.urls import path
from .views import airlines, searched_airlines
from django.views.generic import TemplateView
urlpatterns = [
    path('', airlines, name='airlines'),
    path('search', searched_airlines, name='search_airlines'),
]