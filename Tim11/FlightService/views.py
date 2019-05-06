from django.shortcuts import render, get_object_or_404
from .models import Airline, Flight, FlightReservation
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def airlines(request):
    return render(request, 'airlines_home.html')


def search_flights(request):
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


def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, 'flight_id.html', {'flight':flight})


def search_airlines(request):
    search_input = request.POST.get('airline')
    airlines = Airline.objects.filter(name__contains=search_input)
    return render(request, 'airlines_searched.html', {'airlines': airlines})


def airline_detail(request, airline_id):
    airline = get_object_or_404(Airline, pk=airline_id)
    quick_reservations = FlightReservation.objects.filter(seat__flight__airline=airline, user__isnull=True)
    return render(request, 'airline_id.html', {'airline':airline, 'reservations':quick_reservations})


@login_required
def reserve(request, reservation_id):
    reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    reservation.user = request.user
    reservation.save()
    return render(request, 'airlines_home.html')

def flight_service_reports(request):
    print(datetime.today())
    print(datetime.today() - timedelta(days=1))
    today = FlightReservation.objects.filter(seat__flight__departure_time__lt=datetime.today()) & FlightReservation.objects.filter(seat__flight__departure_time__gt=datetime.today()-timedelta(days=1))
    yesterday = FlightReservation.objects.filter(seat__flight__departure_time__lt=datetime.today() - timedelta(days=1)) & FlightReservation.objects.filter(seat__flight__departure_time__gt=datetime.today()-timedelta(days=2))
    twodaysago = FlightReservation.objects.filter(seat__flight__departure_time__lt=datetime.today() - timedelta(days=2)) & FlightReservation.objects.filter(seat__flight__departure_time__gt=datetime.today()-timedelta(days=3))
    threedaysago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(days=3)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(days=4))
    fourdaysago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(days=4)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(days=5))
    fivedaysago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(days=5)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(days=6))

    oneweekago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today()) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=1))
    twoweeksago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=1)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=2))
    threeweeksago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=2)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=3))
    fourweeksago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=3)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=4))

    onemonthago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today()) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=4))
    twomonthsago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=4)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=8))
    threemonthsago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=8)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=12))
    fourmonthsago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=12)) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=16))

    days = [
        'Today',
        'Yesterday',
        '2 days ago',
        '3 days ago',
        '4 days ago',
        '5 days ago',
    ]
    weeks = [
        'One week ago',
        'Two weeks ago',
        'Three weeks ago',
        'Four weeks ago',
    ]
    months = [
        'One month ago',
        'Two months ago',
        'Three months ago',
        'Four months ago'
    ]
    daysCount = [today.count(), yesterday.count(), twodaysago.count(), threedaysago.count(), fourdaysago.count(),fivedaysago.count()]
    weeksCount = [oneweekago.count(), twoweeksago.count(), threeweeksago.count(), fourweeksago.count()]
    monthsCount = [onemonthago.count(), twomonthsago.count(), threemonthsago.count(), fourmonthsago.count()]
    return JsonResponse({'daysCount': daysCount, 'days': days, 'weeks': weeks, 'weeksCount': weeksCount, 'months': months, 'monthsCount': monthsCount})
