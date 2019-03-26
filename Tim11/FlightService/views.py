from django.shortcuts import render
from .models import Airline
# Create your views here.

def airlines(request):
    return render(request, 'airlines_home.html')

def searched_airlines(request):
    search = request.POST.get('airline_search')
    airlines = Airline.objects.filter(name__contains=search)
    return render(request, 'airlines_searched.html', {'airlines': airlines})
