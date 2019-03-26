from django.shortcuts import render
from .models import RentACar
# Create your views here.

def rentacars(request):
    return render(request, 'rentacar_home.html')

def searched_rentacars(request):
    search = request.POST.get('rentacar_search')
    rentacar_list = RentACar.objects.filter(name__contains=search)
    return render(request, 'rentacar_searched.html', {'rentacars': rentacar_list})
