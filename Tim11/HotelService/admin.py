from django.contrib import admin
from .models import Hotel, HotelAdministrator
from Users.models import CustomUser
from django.contrib.auth.models import Group

class HotelAdministratorInline(admin.StackedInline):
    model = HotelAdministrator
    extra = 0


class HotelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address']
    exclude = ('rating',)
    #readonly_fields = ('rating',)
    inlines = [HotelAdministratorInline]

    def get_queryset(self, request):
        qs = super(HotelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hoteladministrator__user_profile=request.user)


class HotelAdministratorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(HotelAdministratorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user_profile'].queryset = CustomUser.objects.filter(is_staff=True, groups__name='HotelAdministrator')
        return form


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelAdministrator, HotelAdministratorAdmin)
