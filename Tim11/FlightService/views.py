from django.shortcuts import render
from .models import Airline, Flight
from datetime import datetime
# Create your views here.

def airlines(request):
    return render(request, 'airlines_home.html')


def searched_airlines(request):
    destination_from = request.POST.get('destination_from')
    destination_to = request.POST.get('destination_to')
    try:
        date_depart = datetime.strptime(request.POST.get('date_depart'), '%Y-%m-%d')
        flights = Flight.objects.filter(destination_from__name__contains=destination_from,destination_to__name__contains=destination_to,departure_time__day=date_depart.day, departure_time__month=date_depart.month,departure_time__year=date_depart.year)
    except(ValueError):
        flights = Flight.objects.filter(destination_from__name__contains=destination_from,destination_to__name__contains=destination_to)

    try:
        date_return = datetime.strptime(request.POST.get('date_return'), '%Y-%m-%d')
        flights_inv = Flight.objects.filter(destination_from__name__contains=destination_to, destination_to__name__contains=destination_from, departure_time__day=date_return.day, departure_time__month=date_return.month, departure_time__year=date_return.year)
    except(ValueError):
        flights_inv = Flight.objects.filter(destination_from__name__contains=destination_to,destination_to__name__contains=destination_from)

    return render(request, 'airlines_searched.html', {'flights': flights, 'flights_inv:': flights_inv})

