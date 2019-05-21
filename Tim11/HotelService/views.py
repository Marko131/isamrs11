from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, HotelReservation, RoomRating
from django.http import HttpResponseForbidden, JsonResponse
from FlightService.models import FlightReservation
from datetime import datetime, timedelta


def hotels(request):
    return render(request, 'hotels_home.html')


def searched_hotels(request):
    search = request.POST.get('hotels_search')
    hotels_list = Hotel.objects.filter(name__contains=search)
    return render(request, 'hotels_searched.html', {'hotels': hotels_list})


def search_rooms(request):
    flight_reservation_id = request.POST.get('flight_reservation_id')
    print(flight_reservation_id)
    type = request.POST.get('type')
    capacity = request.POST.get('capacity')
    floor = request.POST.get('floor')
    if capacity != "":
        if floor != "":
            rooms = Room.objects.filter(type__contains=type, capacity=capacity, floor=floor)
        else:
            rooms = Room.objects.filter(type__contains=type, capacity=capacity)
    else:
        if floor != "":
            rooms = Room.objects.filter(type__contains=type, floor=floor)
        else:
            rooms = Room.objects.filter(type__contains=type)
    return render(request, 'hotels_searched.html', {'rooms':rooms, 'flight_reservation_id': flight_reservation_id})


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'hotel_id.html', {'hotel': hotel})


def find_rooms(request, flight_reservation_id, passengers):
    flight_reservation = get_object_or_404(FlightReservation, pk=flight_reservation_id)
    if flight_reservation.user != request.user:
        return HttpResponseForbidden()
    quick_reservations = HotelReservation.objects.filter(quick=True, user__isnull=True, room__capacity__gte=passengers, reserved_from=flight_reservation.seat.flight.arrival_time.date())
    return render(request, 'find_rooms.html', {'flight_reservation': flight_reservation_id, 'quick_reservations': quick_reservations, 'passengers': passengers})


def reserve_room(request):
    flight_reservation_id = request.POST.get('flight_reservation_id')
    room_id = request.POST.get('room_id')
    num_days = request.POST.get('num_days')
    flight_reservation = get_object_or_404(FlightReservation, pk=flight_reservation_id)
    room = get_object_or_404(Room, pk=room_id)
    from_date = flight_reservation.seat.flight.arrival_time.date()
    to_date = from_date + timedelta(days=int(num_days))
    room_reservations = HotelReservation.objects.filter(room=room)
    for room_res in room_reservations:
        if from_date > room_res.reserved_to and to_date > room_res.reserved_to:
            continue
        elif from_date < room_res.reserved_from and to_date < room_res.reserved_from:
            continue
        else:
            return JsonResponse({'greska': 'postoji vec rezervacija'})
    hotel_reservation = HotelReservation.objects.create(flight_reservation=flight_reservation, quick=False, room=room, user=flight_reservation.user, reserved_from=from_date, reserved_to=to_date)
    return redirect('my_reservations')


def reserve_quick_room(request):
    flight_reservation_id = request.POST.get('flight_reservation_id')
    room_reservation_id = request.POST.get('room_reservation_id')
    flight_reservation = get_object_or_404(FlightReservation, pk=flight_reservation_id)
    room_reservation = get_object_or_404(HotelReservation, pk=room_reservation_id)
    room_reservation.flight_reservation = flight_reservation
    room_reservation.user = request.user
    room_reservation.save()
    return redirect('my_reservations')

def search_rooms_after_reservation(request):
    flight_reservation_id = request.POST.get('flight_reservation_id')
    print(flight_reservation_id)
    type = request.POST.get('type')
    capacity = request.POST.get('capacity')
    floor = request.POST.get('floor')
    if capacity != "":
        if floor != "":
            rooms = Room.objects.filter(type__contains=type, capacity__gte=capacity, floor=floor)
        else:
            rooms = Room.objects.filter(type__contains=type, capacity__gte=capacity)
    else:
        if floor != "":
            rooms = Room.objects.filter(type__contains=type, floor=floor)
        else:
            rooms = Room.objects.filter(type__contains=type)
    return render(request, 'hotels_searched.html', {'rooms': rooms, 'flight_reservation_id': flight_reservation_id})


def rate_room(request):
    r = request.POST.get('rate')
    room = Room.objects.get(pk=request.POST.get('room_id'))
    room_rating = RoomRating.objects.get_or_create(room=room, user=request.user)
    room_rating = RoomRating.objects.get(room=room, user=request.user)
    room_rating.rate = r
    room_rating.save()
    return JsonResponse({})
