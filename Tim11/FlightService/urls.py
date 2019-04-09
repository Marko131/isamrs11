from django.urls import path
from .views import airlines, searched_airlines
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='airlines_home.html'), name='airlines'),
    path('search', searched_airlines, name='search_airlines'),
]