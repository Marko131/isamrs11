from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Friends, Request
from django.views import View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import PasswordChangeForm
from FlightService.models import FlightReservation
from RentACarService.models import VehicleReservation



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created')
            return redirect('login')
        else:
            return render(request, 'Users/register.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'Users/profile.html', {'form':form})


class FriendList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        friends = Friends.objects.filter(current_user_id=request.user.id).first()
        requests = Request.objects.filter(user_accept_id=request.user.id)
        if friends is not None:
            friends_list = friends.friend_list.all()
        else:
            friends_list = []
        return render(request, 'Users/friends.html', {'friends': friends_list, 'requests': requests})

    def post(self, request, **kwargs):
        search = request.POST.get('search_friend')

        users = CustomUser.objects.filter(Q(first_name__contains=search) | Q(last_name__contains=search)).exclude(pk=request.user.id)
        users_tuple = []
        for user in users:
            user_friends = get_object_or_404(Friends, current_user=request.user)

            if user in list(user_friends.friend_list.all()):
                users_tuple.append([user, 0])
                continue
            else:
                request_send = Request.objects.filter(user_send=request.user, user_accept=user).first()
                if request_send:
                    users_tuple.append([user, 1])
                    continue
                request_get = Request.objects.filter(user_send=user, user_accept=request.user).first()
                if request_get:
                    users_tuple.append([user, 2])
                    continue
                users_tuple.append([user, 3])

        return render(request, 'Users/search_users.html', {'users':users_tuple})

def send_request(request, user_id):
    user_accept = get_object_or_404(CustomUser, pk=user_id)
    Request.objects.create(user_send=request.user, user_accept=user_accept)
    return HttpResponse('')


def ignore_request(request, request_id):
    friend_request = get_object_or_404(Request, pk=request_id)
    friend_request.delete()
    return HttpResponse('')


def accept_request(request, request_id):
    friend_request = get_object_or_404(Request, pk=request_id)
    if friend_request.user_accept != request.user:
        return HttpResponseForbidden()
    friends1, created1 = Friends.objects.get_or_create(current_user=friend_request.user_send)
    friends2, created2 = Friends.objects.get_or_create(current_user=friend_request.user_accept)

    friends1.friend_list.add(friend_request.user_accept)
    friends2.friend_list.add(friend_request.user_send)
    friend_request.delete()
    return HttpResponse('')


def remove_friend(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    friends1 = get_object_or_404(Friends, current_user=request.user)
    friends2 = get_object_or_404(Friends, current_user=user)

    friends1.friend_list.remove(user)
    friends2.friend_list.remove(request.user)

    return HttpResponse('')


def my_reservations(request):
    flight_reservations = FlightReservation.objects.filter(Q(user=request.user, creator=True, accepted=False) | Q(user=request.user, creator=False, accepted=True))
    flight_invites = FlightReservation.objects.filter(user=request.user, creator=False, accepted=False)

    vehicle_reservations = VehicleReservation.objects.filter(user=request.user)
    return render(request, 'Users/my_reservations.html', {'flight_reservations': flight_reservations, 'vehicle_reservations': vehicle_reservations, "flight_invites": flight_invites})


def cancel_resevation(request, reservation_id):
    flight_reservation = get_object_or_404(FlightReservation, pk=reservation_id)
    if flight_reservation.quick:
        flight_reservation.user = None
        flight_reservation.passport = ''
        flight_reservation.accepted = False
        flight_reservation.creator = False
        flight_reservation.save()
    else:
        flight_reservation.delete()

    return redirect('my_reservations')


def cancel_reservation_vehicle(request, reservation_id):
    vehicle_reservation = get_object_or_404(VehicleReservation, pk=reservation_id)
    vehicle_reservation.user = None
    vehicle_reservation.save()
    return redirect('my_reservations')
