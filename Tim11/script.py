import django
import os
import random
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tim11.settings')
django.setup()
from FlightService.models import *
from HotelService.models import *
from RentACarService.models import *
from Users.models import CustomUser
from django.contrib.auth.models import Group, Permission

CustomUser.objects.filter(is_superuser=False).delete()

#Groups
Group.objects.get_or_create(name='AirlineAdministrator')
Group.objects.get_or_create(name='HotelAdministrator')
Group.objects.get_or_create(name='RentACarAdministrator')
Group.objects.get_or_create(name='SystemAdministrator')

airline_admin_permissions = [
    Permission.objects.get(codename='change_airline'),
    Permission.objects.get(codename='view_airline'),
    Permission.objects.get(codename='add_destination'),
    Permission.objects.get(codename='change_destination'),
    Permission.objects.get(codename='delete_destination'),
    Permission.objects.get(codename='view_destination'),
    Permission.objects.get(codename='add_flight'),
    Permission.objects.get(codename='change_flight'),
    Permission.objects.get(codename='delete_flight'),
    Permission.objects.get(codename='view_flight'),
    Permission.objects.get(codename='add_flightreservation'),
    Permission.objects.get(codename='delete_flightreservation'),
    Permission.objects.get(codename='view_flightreservation'),
    Permission.objects.get(codename='view_seat'),
    Permission.objects.get(codename='change_customuser'),
    Permission.objects.get(codename='view_customuser'),
]
airlineadmin_group = Group.objects.get(name='AirlineAdministrator')
for p in airline_admin_permissions:
    airlineadmin_group.permissions.add(p)

hotel_admin_permissions = [
    Permission.objects.get(codename='change_hotel'),
    Permission.objects.get(codename='view_hotel'),
    Permission.objects.get(codename='add_hotelreservation'),
    Permission.objects.get(codename='delete_hotelreservation'),
    Permission.objects.get(codename='view_hotelreservation'),
    Permission.objects.get(codename='add_room'),
    Permission.objects.get(codename='change_room'),
    Permission.objects.get(codename='delete_room'),
    Permission.objects.get(codename='view_room'),
    Permission.objects.get(codename='change_customuser'),
    Permission.objects.get(codename='view_customuser'),
]

hotel_admin_group = Group.objects.get(name='HotelAdministrator')
for p in hotel_admin_permissions:
    hotel_admin_group.permissions.add(p)

rentacar_admin_permissions = [
    Permission.objects.get(codename='add_branch'),
    Permission.objects.get(codename='change_branch'),
    Permission.objects.get(codename='delete_branch'),
    Permission.objects.get(codename='view_branch'),
    Permission.objects.get(codename='change_rentacar'),
    Permission.objects.get(codename='view_rentacar'),
    Permission.objects.get(codename='add_vehicle'),
    Permission.objects.get(codename='change_vehicle'),
    Permission.objects.get(codename='delete_vehicle'),
    Permission.objects.get(codename='view_vehicle'),
    Permission.objects.get(codename='add_vehiclereservation'),
    Permission.objects.get(codename='delete_vehiclereservation'),
    Permission.objects.get(codename='view_vehiclereservation'),
    Permission.objects.get(codename='change_customuser'),
    Permission.objects.get(codename='view_customuser'),
]
rentacar_admin_group = Group.objects.get(name='RentACarAdministrator')
for p in rentacar_admin_permissions:
    rentacar_admin_group.permissions.add(p)

system_admin_permissions = [
    Permission.objects.get(codename='add_airline'),
    Permission.objects.get(codename='delete_airline'),
    Permission.objects.get(codename='view_airline'),
    Permission.objects.get(codename='add_airlineadministrator'),
    Permission.objects.get(codename='change_airlineadministrator'),
    Permission.objects.get(codename='delete_airlineadministrator'),
    Permission.objects.get(codename='view_airlineadministrator'),
    Permission.objects.get(codename='add_hotel'),
    Permission.objects.get(codename='delete_hotel'),
    Permission.objects.get(codename='view_hotel'),
    Permission.objects.get(codename='add_hoteladministrator'),
    Permission.objects.get(codename='change_hoteladministrator'),
    Permission.objects.get(codename='delete_hoteladministrator'),
    Permission.objects.get(codename='view_hoteladministrator'),
    Permission.objects.get(codename='add_rentacar'),
    Permission.objects.get(codename='delete_rentacar'),
    Permission.objects.get(codename='view_rentacar'),
    Permission.objects.get(codename='add_rentacaradministrator'),
    Permission.objects.get(codename='change_rentacaradministrator'),
    Permission.objects.get(codename='delete_rentacaradministrator'),
    Permission.objects.get(codename='view_rentacaradministrator'),
    Permission.objects.get(codename='add_customuser'),
    Permission.objects.get(codename='change_customuser'),
    Permission.objects.get(codename='delete_customuser'),
    Permission.objects.get(codename='view_customuser'),
]
system_admin_group = Group.objects.get(name='SystemAdministrator')

for p in system_admin_permissions:
    system_admin_group.permissions.add(p)

for i in range(5):
    CustomUser.objects.create_user(email=f'systemadmin{i}@gmail.com', password='marko123', first_name=f'FirstName{i}', last_name=f'LastName{i}', is_staff=True)

system_admin_list = list(CustomUser.objects.filter(email__contains='systemadmin'))
for s in system_admin_list:
    system_admin_group.user_set.add(s)

#FlightService
for i in range(10):
    a, created = Airline.objects.get_or_create(name=f'Airline{i}', address=f'Address{i}', description=f'Description{i}')
print('Airlines created')

airline_list = list(Airline.objects.all())
for i in range(10):
    d, created = Destination.objects.get_or_create(name=f'Destination{i}', country=f'Country{i}', airport=f'Airport{i}', airport_code=f'Code{i}', airline=random.choice(airline_list))
print('Destinations created')

destination_list = list(Destination.objects.all())

for i in range(20):
    u = CustomUser.objects.create_user(email=f'airlineadmin{i}@gmail.com', password='marko123', first_name=f'FirstName{i}', last_name=f'LastName{i}', is_staff=True)


users_list = list(CustomUser.objects.filter(email__contains='airlineadmin'))

for u in users_list:
    AirlineAdministrator.objects.get_or_create(user_profile=u, airline=random.choice(airline_list))

day = 5
for i in range(50):
    if i % 4 == 0:
        day += 1
    destination_from = random.choice(destination_list)
    destination_to = random.choice(destination_list)
    if destination_from.name == destination_to.name:
        continue
    d_time = datetime.now() + timedelta(days=day)
    a_time = datetime.now() + timedelta(days=day) + timedelta(hours=5)

    rf = random.randint(0,5)
    cf = random.randint(0, 5)
    if rf == 0 or cf == 0:
        rf = cf = 0

    rb = random.randint(0, 5)
    cb = random.randint(0, 5)
    if rb == 0 or cb == 0:
        rb = cb = 0

    re = random.randint(0, 5)
    ce = random.randint(0, 5)
    if re == 0 or ce == 0:
        re = ce = 0

    d = random.randint(5, 30)
    b = random.randint(10, 30)
    f, created = Flight.objects.get_or_create(destination_from=destination_from, destination_to=destination_to, departure_time=d_time, arrival_time=a_time, flight_distance=300, price=500, airline=random.choice(airline_list), rows_economy=re, cols_economy=ce, rows_business=rb, cols_business=cb, rows_first=rf, cols_first=cf, discount=d, checked_baggage=b)

#HotelService

destination_names = [[d.name, d.country] for d in Destination.objects.all()]
Hotel.objects.all().delete()
for i in range(10):
    destination = random.choice(destination_names)
    h, created = Hotel.objects.get_or_create(name=f'Hotel{i}',
                                             address=f'Address{i}',
                                             description=f'Description{i}',
                                             city=destination[0],
                                             country=destination[1],
                                             airport_transfer=bool(random.getrandbits(1)),
                                             airport_transfer_price=random.randint(5, 10),
                                             parking=bool(random.getrandbits(1)),
                                             parking_price=random.randint(5, 10),
                                             pool=bool(random.getrandbits(1)),
                                             pool_price=random.randint(5, 10),
                                             restaurant=bool(random.getrandbits(1)),
                                             restaurant_price=random.randint(5, 10),
                                             room_service=bool(random.getrandbits(1)),
                                             room_service_price=random.randint(5, 10),
                                             gym=bool(random.getrandbits(1)),
                                             gym_price=random.randint(5, 10),
                                             spa=bool(random.getrandbits(1)),
                                             spa_price=random.randint(5, 10),
                                             wifi=bool(random.getrandbits(1)),
                                             wifi_price=random.randint(5, 10),
                                             )

list_of_hotels = list(Hotel.objects.all())
types_list = [('One bed', 1), ('Two bed', 2), ('Three bed', 3), ('Four bed', 4)]
Room.objects.all().delete()
for i in range(50):
    room_type = random.choice(types_list)
    r, created = Room.objects.get_or_create(type=room_type[0],
                                            capacity=room_type[1],
                                            floor=random.randint(0, 10),
                                            balcony=bool(random.getrandbits(1)),
                                            price=random.randint(50, 200),
                                            hotel = random.choice(list_of_hotels),
                                            discount=random.randint(5, 20)
                                            )


for i in range(20):
    CustomUser.objects.create_user(email=f'hoteladmin{i}@gmail.com', password="marko123", is_staff=True)


HotelAdministrator.objects.all().delete()
users_list2 = list(CustomUser.objects.filter(email__contains='hoteladmin'))
for u in users_list2:
    HotelAdministrator.objects.get_or_create(user_profile=u, hotel=random.choice(list_of_hotels))


#RentACarService
for i in range(20):
    CustomUser.objects.create_user(email=f'rentacar{i}@gmail.com', password="marko123", is_staff=True)
users_list3 = list(CustomUser.objects.filter(email__contains='rentacar'))

for i in range(10):
    RentACar.objects.get_or_create(name=f'RentACar{i}', address=f'Address{i}', description=f'Description{i}')

list_of_rentacars = list(RentACar.objects.all())
for i in range(20):
    destination = random.choice(destination_names)
    Branch.objects.get_or_create(name=destination[0], country=destination[1], rentacar=random.choice(list_of_rentacars))

for i in range(50):
    Vehicle.objects.get_or_create(price=random.randint(30, 100),
                                  manufacturer=f'Manufacturer{i}',
                                  model_name=f'Model{i}',
                                  capacity=random.randint(2, 9),
                                  rentacar=random.choice(list_of_rentacars),
                                  discount=random.randint(5, 30),
    )

for u in users_list3:
    RentACarAdministrator.objects.get_or_create(user_profile=u, rentacarservice=random.choice(list_of_rentacars))

