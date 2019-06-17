from django.contrib import admin
from .models import Hotel, HotelAdministrator, Room, HotelReservation, RoomRating
from Users.models import CustomUser
from django.contrib.auth.models import Group

class HotelAdministratorInline(admin.StackedInline):
    model = HotelAdministrator
    extra = 0


class HotelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address']
    exclude = ('rating',)
    inlines = [HotelAdministratorInline]

    def get_queryset(self, request):
        qs = super(HotelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hoteladministrator__user_profile=request.user)


class HotelAdministratorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(HotelAdministratorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user_profile'].queryset = CustomUser.objects.filter(is_staff=True, groups__isnull=True, is_superuser=False)
        return form


class RoomAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['hotel']
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.hotel = request.user.hoteladministrator.hotel
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(RoomAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hotel=request.user.hoteladministrator.hotel)


class HotelReservationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(HotelReservationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(room__hotel=request.user.hoteladministrator.hotel)


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelAdministrator, HotelAdministratorAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(HotelReservation, HotelReservationAdmin)
admin.site.register(RoomRating)
