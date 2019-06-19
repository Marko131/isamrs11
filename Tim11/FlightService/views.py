from django.shortcuts import render, get_object_or_404, redirect
from .models import Airline, Flight, FlightReservation, FlightRating, Seat
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from Users.models import CustomUser
import threading
from django.core.mail import EmailMessage
from Tim11.settings import EMAIL_HOST_USER
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Sum
from Users.models import Friends

def airlines(request):
    airline = Airline.objects.order_by('-pk')[:3]
    return render(request, 'airlines_home.html', {'airlines': airline})

def search_flights(request):
    destination_from = request.GET.get('destination_from')
    destination_to = request.GET.get('destination_to')
    multi_city = request.GET.get('multi_city')
    try:
        date_depart = datetime.strptime(request.GET.get('date_depart'), '%Y-%m-%d')
        if multi_city is not None:
            flights = Flight.objects.filter(destination_from__name__contains=destination_from,destination_to__name__contains=destination_to,departure_time__day=date_depart.day, departure_time__month=date_depart.month,departure_time__year=date_depart.year, departure_time__gt=datetime.now())
        else:
            flights = Flight.objects.filter(destination_from__name__contains=destination_from,destination_to__name__contains=destination_to,departure_time__day=date_depart.day, departure_time__month=date_depart.month,departure_time__year=date_depart.year, connections__isnull=True, departure_time__gt=datetime.now())
    except ValueError:
        if multi_city is not None:
            flights = Flight.objects.filter(destination_from__name__contains=destination_from,destination_to__name__contains=destination_to, departure_time__gt=datetime.now())
        else:
            flights = Flight.objects.filter(destination_from__name__contains=destination_from,destination_to__name__contains=destination_to, connections__isnull=True, departure_time__gt=datetime.now())


    try:
        date_return = datetime.strptime(request.GET.get('date_return'), '%Y-%m-%d')
        if multi_city is not None:
            flights_inv = Flight.objects.filter(destination_from__name__contains=destination_to, destination_to__name__contains=destination_from, departure_time__day=date_return.day, departure_time__month=date_return.month, departure_time__year=date_return.year, departure_time__gt=datetime.now())
        else:
            flights_inv = Flight.objects.filter(destination_from__name__contains=destination_to, destination_to__name__contains=destination_from, departure_time__day=date_return.day, departure_time__month=date_return.month, departure_time__year=date_return.year, connections__isnull=True, departure_time__gt=datetime.now())
        flights = flights | flights_inv
    except ValueError:
        pass

    economy = request.GET.get('economy')
    business = request.GET.get('business')
    first = request.GET.get('first')
    checked_baggage = request.GET.get('checked_baggage')
    passengers = request.GET.get('passengers')


    if checked_baggage:
        flights = flights.filter(checked_baggage__gte=checked_baggage)

    if economy is not None:
        flights = flights.filter(rows_economy__gt=0, cols_economy__gt=0)

    if business is not None:
        flights = flights.filter(rows_business__gt=0, cols_business__gt=0)

    if first is not None:
        flights = flights.filter(rows_first__gt=0, cols_first__gt=0)

    try:
        flights = [x for x in flights if x.seats_count > int(passengers)]
    except TypeError:
        pass
    except ValueError:
        pass

    paginator = Paginator(list(flights), 5)
    page = request.GET.get('page')
    flights = paginator.get_page(page)
    return render(request, 'airlines_searched.html', {'flights': flights})

@login_required
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    friends = get_object_or_404(Friends, current_user=request.user)
    return render(request, 'flight_id.html', {'flight':flight, 'friends': friends.friend_list.all()})


def search_airlines(request):
    search_input = request.GET.get('airline')
    airlines = Airline.objects.filter(name__contains=search_input)
    return render(request, 'airlines_searched.html', {'airlines': airlines})


def airline_detail(request, airline_id):
    airline = get_object_or_404(Airline, pk=airline_id)
    quick_reservations = FlightReservation.objects.filter(seat__flight__airline=airline, user__isnull=True, seat__flight__departure_time__gt=datetime.now())
    return render(request, 'airline_id.html', {'airline':airline, 'reservations': quick_reservations})


@login_required
@transaction.atomic
def reserve(request, reservation_id):
    reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    reservation.user = request.user
    passport = request.POST.get("passport")
    reservation.passport = passport
    reservation.accepted = False
    reservation.creator = True
    reservation.date_created = datetime.today()
    reservation.save()
    return render(request, 'airlines_home.html')


def flight_service_reports(request):
    date_from_day = int(request.GET.get('date_from_day'))
    date_from_month = int(request.GET.get('date_from_month'))
    date_from_year = int(request.GET.get('date_from_year'))

    date_to_day = int(request.GET.get('date_to_day'))
    date_to_month = int(request.GET.get('date_to_month'))
    date_to_year = int(request.GET.get('date_to_year'))

    airline_id = request.GET.get('airline_id')
    date_from = datetime(day=date_from_day, month=date_from_month, year=date_from_year)
    date_to = datetime(day=date_to_day, month=date_to_month, year=date_to_year)

    qs = FlightReservation.objects.filter(seat__flight__airline_id=airline_id, date_created__gte=date_from, date_created__lte=date_to).aggregate(Sum('seat__flight__price'))
    #FlightRating.objects.filter(flight__airline=obj).aggregate(Avg('rate'))['rate__avg']
    return JsonResponse({'result': qs.get('seat__flight__price__sum')})


@login_required
def rate_flight(request):
    r = request.POST.get('rate')
    flight = Flight.objects.get(pk=request.POST.get('flight_id'))
    flight_rating = FlightRating.objects.get_or_create(flight=flight, user=request.user)
    flight_rating = FlightRating.objects.get(flight=flight, user=request.user)
    flight_rating.rate = r
    flight_rating.save()
    return JsonResponse({})


@login_required
@transaction.atomic
def finish_flight_reservation(request):
    seats = request.POST.getlist('seats[]')
    invited_friends = request.POST.getlist('invited_friends[]')
    getUrl = request.get_host()
    invited_friends.insert(0, request.user.email)
    passport = request.POST.get("passport")
    if not seats or not invited_friends or len(seats) != len(invited_friends):
        response = JsonResponse({'Error': 'No selected seats'})
        response.status_code = 403
        return response
    my_reservation_id = None
    for s, i in zip(seats, invited_friends):
        if not i:
            response = JsonResponse({'Error': 'Number of seats and passengers don\'t match'})
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
                                   f"<a href=\"{getUrl}/invite/{flight_reservation.id}\"> Click here to accept or cancel the invite. </a>",
                                   [i])
        except:
            flight_reservation = FlightReservation.objects.create(seat=seat, user=None, accepted=False, creator=False, quick=False)
            send_html_mail("Flight invite", f"<a href=\"{getUrl}/invite/{flight_reservation.id}\"> Click here to accept or cancel the invite. </a>", [i])
    if my_reservation_id is not None:
        response = JsonResponse({'passengers': len(seats), 'flight_reservation_id': my_reservation_id})
    else:
        response = JsonResponse({'Error': 'Something went wrong'})
        response.status_code = 403
    return response


@login_required
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


@login_required
def get_rating_airline(request):
    if not request.user.is_superuser:
        rating_qs = FlightRating.objects.filter(flight__airline=request.user.airlineadministrator.airline)
        rating_list = [r.rate for r in rating_qs]
        rating = float(sum(rating_list)) / len(rating_list)
        return JsonResponse({'rating': rating})
    else:
        return HttpResponseBadRequest()


