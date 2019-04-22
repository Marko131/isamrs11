from django.shortcuts import render, get_object_or_404
from .models import RentACar, Vehicle
# Create your views here.

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
    return render(request, 'rentacar_id.html', {'rentacar': rentacar})
