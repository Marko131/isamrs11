from django.shortcuts import render
from .models import Hotel
# Create your views here.

def hotels(request):
    return render(request, 'hotels_home.html')

def searched_hotels(request):
    search = request.POST.get('hotels_search')
    hotels_list = Hotel.objects.filter(name__contains=search)
    return render(request, 'hotels_searched.html', {'hotels': hotels_list})

