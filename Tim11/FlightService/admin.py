from django.contrib import admin
from .models import Destination, Airline, AirlineAdministrator, Flight, Seat, FlightReservation, FlightRating
from Users.models import CustomUser
from django.contrib.auth.models import Group
from django.db.models import Avg
from datetime import datetime, timedelta
from .forms import FlightAdminForm, CalculateForm

class AirlineAdministratorInline(admin.TabularInline):
    model = AirlineAdministrator
    extra = 0


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0


class AircraftModelAdmin(admin.ModelAdmin):
    inlines = [SeatInline]


class AirlineAdmin(admin.ModelAdmin):
    list_display = ['name', 'average_rate']
    fields = ['name', 'address', 'description', 'image', 'rating']
    search_fields = ['name']
    inlines = [AirlineAdministratorInline]

    def average_rate(self, obj):
        return FlightRating.objects.filter(flight__airline=obj).aggregate(Avg('rate'))['rate__avg']
    average_rate.short_description = "Average rate"

    def get_queryset(self, request):
        qs = super(AirlineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airlineadministrator__user_profile=request.user)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        avg_rate = FlightRating.objects.filter(flight__airline=obj).aggregate(Avg('rate'))['rate__avg']
        context['adminform'].form.initial['rating'] = str(avg_rate)
        context['adminform'].form.fields['rating'].disabled = True
        return super(AirlineAdmin, self).render_change_form(request, context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        calculate_form = CalculateForm()
        extra_context['calculate_form'] = calculate_form
        extra_context['airline_id'] = object_id

        today = FlightReservation.objects.filter(date_created=datetime.today(), seat__flight__airline_id=object_id) & FlightReservation.objects.filter(date_created__gt=datetime.today()-timedelta(days=1), seat__flight__airline_id=object_id)
        extra_context['today'] = today.count()

        yesterday = FlightReservation.objects.filter(date_created__lte=datetime.today() - timedelta(days=1), seat__flight__airline_id=object_id) & FlightReservation.objects.filter(date_created__gt=datetime.today()-timedelta(days=2), seat__flight__airline_id=object_id)
        extra_context['yesterday'] = yesterday.count()

        twodaysago = FlightReservation.objects.filter(date_created__lte=datetime.today() - timedelta(days=2), seat__flight__airline_id=object_id) & FlightReservation.objects.filter(date_created__gt=datetime.today()-timedelta(days=3), seat__flight__airline_id=object_id)
        extra_context['twodaysago'] = twodaysago.count()

        threedaysago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(days=3),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(days=4), seat__flight__airline_id=object_id)
        extra_context['threedaysago'] = threedaysago.count()

        fourdaysago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(days=4),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(days=5), seat__flight__airline_id=object_id)
        extra_context['fourdaysago'] = fourdaysago.count()

        fivedaysago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(days=5),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(days=6), seat__flight__airline_id=object_id)
        extra_context['fivedaysago'] = fivedaysago.count()

        oneweekago = FlightReservation.objects.filter(
            date_created__lte=datetime.today(),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=1), seat__flight__airline_id=object_id)
        extra_context['oneweekago'] = oneweekago.count()

        twoweeksago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(weeks=1),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=2), seat__flight__airline_id=object_id)
        extra_context['twoweeksago'] = twoweeksago.count()

        threeweeksago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(weeks=2),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=3), seat__flight__airline_id=object_id)
        extra_context['threeweeksago'] = threeweeksago.count()

        fourweeksago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(weeks=3),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=4), seat__flight__airline_id=object_id)
        extra_context['fourweeksago'] = fourweeksago.count()

        onemonthago = FlightReservation.objects.filter(
            date_created__lte=datetime.today(),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=4), seat__flight__airline_id=object_id)
        extra_context['onemonthago'] = onemonthago.count()

        twomonthsago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(weeks=4),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=8), seat__flight__airline_id=object_id)
        extra_context['twomonthsago'] = twomonthsago.count()

        threemonthsago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(weeks=8),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=12), seat__flight__airline_id=object_id)
        extra_context['threemonthsago'] = threemonthsago.count()

        fourmonthsago = FlightReservation.objects.filter(
            date_created__lte=datetime.today() - timedelta(weeks=12),
            seat__flight__airline_id=object_id) & FlightReservation.objects.filter(
            date_created__gt=datetime.today() - timedelta(weeks=16), seat__flight__airline_id=object_id)
        extra_context['fourmonthsago'] = fourmonthsago.count()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class DestinationAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['airline']
        else:
            return []

    def get_queryset(self, request):
        qs = super(DestinationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airline=request.user.airlineadministrator.airline)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.airline = request.user.airlineadministrator.airline
        super().save_model(request, obj, form, change)


class FlightAdmin(admin.ModelAdmin):
    form = FlightAdminForm
    list_display = ('get_name', 'destination_from', 'destination_to', 'departure_time', 'arrival_time', 'average_rate')

    def average_rate(self, obj):

        return FlightRating.objects.filter(flight=obj).aggregate(Avg('rate'))['rate__avg']
    average_rate.short_description = "Average rate"

    def get_name(self, obj):
        return f'Flight ID - {obj.pk}'
    get_name.short_description = 'Flight'

    def get_queryset(self, request):
        qs = super(FlightAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airline=request.user.airlineadministrator.airline)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['airline']
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.airline = request.user.airlineadministrator.airline
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FlightAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['destination_from'].queryset = Destination.objects.filter(airline=request.user.airlineadministrator.airline)
        form.base_fields['destination_to'].queryset = Destination.objects.filter(airline=request.user.airlineadministrator.airline)
        return form


class AirlineAdministratorAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'airline']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(AirlineAdministratorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user_profile'].queryset = CustomUser.objects.filter(is_staff=True, groups__isnull=True, is_superuser=False)
        return form


class SeatAdmin(admin.ModelAdmin):
    list_display = ['link', 'type', 'row', 'col', 'flight', 'available']
    readonly_fields = ['type', 'flight', 'row', 'col', 'available']
    list_filter = ['flight']


    def link(self, obj):
        return 'Select seat'

    def get_queryset(self, request):
        qs = super(SeatAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(flight__airline=request.user.airlineadministrator.airline)


class FlightReservationAdmin(admin.ModelAdmin):
    readonly_fields = ['user']

    def get_queryset(self, request):
        qs = super(FlightReservationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(seat__flight__airline=request.user.airlineadministrator.airline)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FlightReservationAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            form.base_fields['seat'].queryset = Seat.objects.filter(available=True)
            return form
        form.base_fields['seat'].queryset = Seat.objects.filter(flight__airline=request.user.airlineadministrator.airline, available=True)
        return form

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(AirlineAdministrator, AirlineAdministratorAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(FlightReservation, FlightReservationAdmin)
admin.site.register(FlightRating)
