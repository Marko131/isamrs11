import django
import os
import random
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tim11.settings')
django.setup()
from FlightService.models import *
from Users.models import CustomUser

for i in range(10):
    a, created = Airline.objects.get_or_create(name=f'Airline{i}', address=f'Address{i}', description=f'Description{i}')

airline_list = list(Airline.objects.all())

for i in range(10):
    d, created = Destination.objects.get_or_create(name=f'Destination{i}', country=f'Country{i}', airport=f'Airport{i}', airport_code=f'Code{i}', airline=random.choice(airline_list))

destination_list = list(Destination.objects.all())

#Kreiranje korisnika koji ce biti administratori aviokompanija
'''
for i in range(20):
    u = CustomUser.objects.create_user(email=f'airlineadmin{i}@gmail.com', password='marko123', first_name=f'FirstName{i}', last_name=f'LastName{i}', is_staff=True)
'''

users_list = list(CustomUser.objects.filter(email__contains='airlineadmin', airlineadministrator__isnull=True))

for u in users_list:
    AirlineAdministrator.objects.get_or_create(user_profile=u, airline=random.choice(airline_list))

day = 5
for i in range(50):
    if i % 4 == 0:
        day += 1
    destination_from = random.choice(destination_list)
    temp = destination_list
    temp.remove(destination_from)
    destination_to = random.choice(temp)
    d_time = datetime.now() + timedelta(days=day)
    a_time = datetime.now() + timedelta(days=day) + timedelta(hours=5)
    f, created = Flight.objects.get_or_create(destination_from=destination_from, destination_to=destination_to, departure_time=d_time, arrival_time=a_time, flight_distance=300, price=500, airline=random.choice(airline_list), rows_economy=3, cols_economy=3, rows_business=3, cols_business=3, rows_first=3, cols_first=3, discount=20)
