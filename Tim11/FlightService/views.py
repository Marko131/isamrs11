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
    passport = request.POST.get("passport")
    reservation.passport = passport
    reservation.accepted = True
    reservation.creator = True
    reservation.save()
    return render(request, 'airlines_home.html')

def flight_service_reports(request):
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


def rate_flight(request):
    r = request.POST.get('rate')
    flight = Flight.objects.get(pk=request.POST.get('flight_id'))
    flight_rating = FlightRating.objects.get_or_create(flight=flight, user=request.user)
    flight_rating = FlightRating.objects.get(flight=flight, user=request.user)
    flight_rating.rate = r
    flight_rating.save()
    return JsonResponse({})


def finish_flight_reservation(request):
    seats = request.POST.getlist('seats[]')
    invited_friends = request.POST.getlist('invited_friends[]')
    invited_friends.insert(0, request.user.email)
    passport = request.POST.get("passport")
    if not seats or not invited_friends or len(seats) != len(invited_friends):
        return HttpResponse("error")

    for s, i in zip(seats, invited_friends):
        if not i:
            return HttpResponse("Error")
        seat = Seat.objects.get(pk=s)
        try:
            user = CustomUser.objects.get(email=i)
            if user == request.user:
                FlightReservation.objects.create(seat=seat, user=user, accepted=False, passport=passport, creator=True, quick=False)
            else:
                flight_reservation = FlightReservation.objects.create(seat=seat, user=user, accepted=False, quick=False, creator=False)
                if not user.is_active:
                    send_html_mail("Flight invite",
                                   f"<a href=\"http://127.0.0.1:8000/invite/{flight_reservation.id}\"> Hram 3 slova </a>",
                                   [i])
        except:
            flight_reservation = FlightReservation.objects.create(seat=seat, user=request.user, accepted=False, creator=False, quick=False)
            send_html_mail("Flight invite", f"<a href=\"http://127.0.0.1:8000/invite/{flight_reservation.id}\"> Hram 3 slova </a>", [i])
    return render(request, "Users/my_reservations.html")


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
    return HttpResponse("")


def cancel_invite(request, reservation_id):
    flight_reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    flight_reservation.delete()
    return HttpResponse("")
