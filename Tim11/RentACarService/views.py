from django.shortcuts import render, get_object_or_404
from .models import RentACar, Vehicle, VehicleReservation, VehicleRating
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse

def rentacars(request):
    return render(request, 'rentacar_home.html')

def searched_rentacars(request):
    search = request.POST.get('rentacar_search')
    rentacar_list = RentACar.objects.filter(name__contains=search)
    return render(request, 'rentacar_searched.html', {'rentacars': rentacar_list})

def search_vehicles(request):
    manufacturer = request.POST.get('manufacturer')
    model = request.POST.get('model_name')
    vehicles = Vehicle.objects.filter(manufacturer__contains=manufacturer, model_name__contains=model)
    return render(request, 'rentacar_searched.html', {'vehicles': vehicles})

def rentacar_detail(request, rentacar_id):
    rentacar = get_object_or_404(RentACar, pk=rentacar_id)
    quick_reservations = VehicleReservation.objects.filter(vehicle__rentacar=rentacar, user__isnull=True)
    return render(request, 'rentacar_id.html', {'rentacar': rentacar, 'reservations':quick_reservations})

@login_required
def reserve(request, reservation_id):
    reservation = get_object_or_404(VehicleReservation, pk=reservation_id)
    reservation.user = request.user
    reservation.save()
    return render(request, 'rentacar_home.html')

def rentacar_service_reports(request):
    today = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today()) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(days=1))
    yesterday = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(days=1)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(days=2))
    twodaysago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(days=2)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(days=3))
    threedaysago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(days=3)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(days=4))
    fourdaysago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(days=4)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(days=5))
    fivedaysago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(days=5)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(days=6))

    oneweekago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today()) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=1))
    twoweeksago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(weeks=1)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=2))
    threeweeksago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(weeks=2)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=3))
    fourweeksago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(weeks=3)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=4))

    onemonthago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today()) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=4))
    twomonthsago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(weeks=4)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=8))
    threemonthsago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(weeks=8)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=12))
    fourmonthsago = VehicleReservation.objects.filter(
        reserved_from__lt=datetime.today() - timedelta(weeks=12)) & VehicleReservation.objects.filter(
        reserved_from__gt=datetime.today() - timedelta(weeks=16))

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
    days_count = [today.count(), yesterday.count(), twodaysago.count(), threedaysago.count(), fourdaysago.count(),
                 fivedaysago.count()]
    weeks_count = [oneweekago.count(), twoweeksago.count(), threeweeksago.count(), fourweeksago.count()]
    months_count = [onemonthago.count(), twomonthsago.count(), threemonthsago.count(), fourmonthsago.count()]
    return JsonResponse(
        {'daysCount': days_count, 'days': days, 'weeks': weeks, 'weeksCount': weeks_count, 'months': months,
         'monthsCount': months_count})


def rate_vehicle(request):
    r = request.POST.get('rate')
    vehicle = Vehicle.objects.get(pk=request.POST.get('vehicle_id'))
    vehicle_rating = VehicleRating.objects.get_or_create(vehicle=vehicle, user=request.user)
    vehicle_rating = VehicleRating.objects.get(vehicle=vehicle, user=request.user)
    vehicle_rating.rate = r
    vehicle_rating.save()
    return JsonResponse({})
