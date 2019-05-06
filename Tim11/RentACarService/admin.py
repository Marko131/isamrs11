from django.contrib import admin
from .models import RentACar, Branch, Vehicle, RentACarAdministrator, VehicleReservation
from django.contrib import admin
from Users.models import CustomUser
from django.contrib.auth.models import Group

class RentACarAdministratorInline(admin.StackedInline):
    model = RentACarAdministrator
    extra = 0


class RentACarAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address']
    exclude = ('rating',)
    #readonly_fields = ('rating',)
    inlines = [RentACarAdministratorInline]

    def get_queryset(self, request):
        qs = super(RentACarAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(rentacaradministrator__user_profile=request.user)


class RentACarAdministratorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(RentACarAdministratorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user_profile'].queryset = CustomUser.objects.filter(is_staff=True, groups__isnull=True, is_superuser=False)
        return form

class BranchAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['rentacar']
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.rentacar = request.user.rentacaradministrator.rentacarservice
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BranchAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(rentacar=request.user.rentacaradministrator.rentacarservice)

class VehicleAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['rentacar']
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.rentacar = request.user.rentacaradministrator.rentacarservice
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(VehicleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(rentacar=request.user.rentacaradministrator.rentacarservice)


class VehicleReservationAdmin(admin.ModelAdmin):
    readonly_fields = ["user"]

    def get_queryset(self, request):
        qs = super(VehicleReservationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(vehicle__rentacar=request.user.rentacaradministrator.rentacarservice)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(VehicleReservationAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['vehicle'].queryset = Vehicle.objects.filter(rentacar=request.user.rentacaradministrator.rentacarservice)
        return form


admin.site.register(RentACar, RentACarAdmin)
admin.site.register(RentACarAdministrator, RentACarAdministratorAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleReservation, VehicleReservationAdmin)
