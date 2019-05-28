from django.shortcuts import render, get_object_or_404, redirect
from .models import Airline, Flight, FlightReservation, FlightRating, Seat
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Users.models import CustomUser
import threading
from django.core.mail import EmailMessage
from Tim11.settings import EMAIL_HOST_USER
from django.db import transaction


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
    flights = flights.filter(departure_time__gt=datetime.now())

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
    quick_reservations = FlightReservation.objects.filter(seat__flight__airline=airline, user__isnull=True, seat__flight__departure_time__gt=datetime.now())
    return render(request, 'airline_id.html', {'airline':airline, 'reservations':quick_reservations})


@login_required
def reserve(request, reservation_id):
    reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    reservation.user = request.user
    passport = request.POST.get("passport")
    reservation.passport = passport
    reservation.accepted = False
    reservation.creator = True
    reservation.save()
    return render(request, 'airlines_home.html')


def flight_service_reports(request):
    if not request.user.is_superuser:
        airline = request.user.airlineadministrator.airline
    else:
        return JsonResponse({})
    today = FlightReservation.objects.filter(seat__flight__departure_time__lt=datetime.today(), seat__flight__airline=airline) & FlightReservation.objects.filter(seat__flight__departure_time__gt=datetime.today()-timedelta(days=1), seat__flight__airline=airline)
    yesterday = FlightReservation.objects.filter(seat__flight__departure_time__lt=datetime.today() - timedelta(days=1), seat__flight__airline=airline) & FlightReservation.objects.filter(seat__flight__departure_time__gt=datetime.today()-timedelta(days=2), seat__flight__airline=airline)
    twodaysago = FlightReservation.objects.filter(seat__flight__departure_time__lt=datetime.today() - timedelta(days=2), seat__flight__airline=airline) & FlightReservation.objects.filter(seat__flight__departure_time__gt=datetime.today()-timedelta(days=3), seat__flight__airline=airline)
    threedaysago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(days=3), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(days=4), seat__flight__airline=airline)
    fourdaysago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(days=4), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(days=5), seat__flight__airline=airline)
    fivedaysago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(days=5), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(days=6), seat__flight__airline=airline)

    oneweekago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today(), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=1), seat__flight__airline=airline)
    twoweeksago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=1), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=2), seat__flight__airline=airline)
    threeweeksago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=2), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=3), seat__flight__airline=airline)
    fourweeksago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=3), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=4), seat__flight__airline=airline)

    onemonthago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today(), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=4), seat__flight__airline=airline)
    twomonthsago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=4), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=8), seat__flight__airline=airline)
    threemonthsago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=8), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=12), seat__flight__airline=airline)
    fourmonthsago = FlightReservation.objects.filter(
        seat__flight__departure_time__lt=datetime.today() - timedelta(weeks=12), seat__flight__airline=airline) & FlightReservation.objects.filter(
        seat__flight__departure_time__gt=datetime.today() - timedelta(weeks=16), seat__flight__airline=airline)

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


def rate_flight(request):
    r = request.POST.get('rate')
    flight = Flight.objects.get(pk=request.POST.get('flight_id'))
    flight_rating = FlightRating.objects.get_or_create(flight=flight, user=request.user)
    flight_rating = FlightRating.objects.get(flight=flight, user=request.user)
    flight_rating.rate = r
    flight_rating.save()
    return JsonResponse({})


@transaction.atomic
def finish_flight_reservation(request):
    seats = request.POST.getlist('seats[]')
    invited_friends = request.POST.getlist('invited_friends[]')
    invited_friends.insert(0, request.user.email)
    passport = request.POST.get("passport")
    if not seats or not invited_friends or len(seats) != len(invited_friends):
        response = JsonResponse({'Error': 'No selected seats'})
        response.status_code = 403
        return response
    my_reservation_id = None
    for s, i in zip(seats, invited_friends):
        if not i:
            response = JsonResponse({'Error': 'Number of seats and passengers doesn\'t match'})
            response.status_code = 403
            return response
        seat = Seat.objects.get(pk=s)
        try:
            user = CustomUser.objects.get(email=i)
            if user == request.user:
                fr = FlightReservation.objects.create(seat=seat, user=user, accepted=False, passport=passport, creator=True, quick=False)
                my_reservation_id = fr.pk
            else:
                flight_reservation = FlightReservation.objects.create(seat=seat, user=user, accepted=False, quick=False, creator=False)
                if not user.is_active:
                    send_html_mail("Flight invite",
                                   f"<a href=\"http://127.0.0.1:8000/invite/{flight_reservation.id}\"> Click here to accept or cancel the invite. </a>",
                                   [i])
        except:
            flight_reservation = FlightReservation.objects.create(seat=seat, user=None, accepted=False, creator=False, quick=False)
            send_html_mail("Flight invite", f"<a href=\"http://127.0.0.1:8000/invite/{flight_reservation.id}\"> Click here to accept or cancel the invite. </a>", [i])
    if my_reservation_id is not None:
        response = JsonResponse({'passengers': len(seats), 'flight_reservation_id': my_reservation_id})
    else:
        response = JsonResponse({'Error': 'Something went wrong'})
        response.status_code = 403
    return response


def invite(request, reservation_id):
    get_object_or_404(FlightReservation, pk=reservation_id)
    return render(request, "invite.html", {"reservation_id": reservation_id})


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()


def accept_invite(request, reservation_id):
    passport = request.POST.get("passport")
    flight_reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    flight_reservation.accepted = True
    flight_reservation.passport = passport
    flight_reservation.save()
    return redirect("airlines")


def cancel_invite(request, reservation_id):
    flight_reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    flight_reservation.delete()
    return redirect("airlines")

def get_rating_airline(request):
    if not request.user.is_superuser:
        rating_qs = FlightRating.objects.filter(flight__airline=request.user.airlineadministrator.airline)
        rating_list = [r.rate for r in rating_qs]
        rating = float(sum(rating_list)) / len(rating_list)
        return JsonResponse({'rating': rating})
    else:
        return JsonResponse({'rating': 0})


