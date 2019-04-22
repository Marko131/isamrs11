from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room
# Create your views here.

def hotels(request):
    return render(request, 'hotels_home.html')

def searched_hotels(request):
    search = request.POST.get('hotels_search')
    hotels_list = Hotel.objects.filter(name__contains=search)
    return render(request, 'hotels_searched.html', {'hotels': hotels_list})

def search_rooms(request):
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
    return render(request, 'hotels_searched.html', {'rooms':rooms})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'hotel_id.html', {'hotel': hotel})
