from django.contrib import admin
from .models import RentACar, Branch
from django.contrib import admin
from .models import RentACar, RentACarAdministrator
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
        form.base_fields['user_profile'].queryset = CustomUser.objects.filter(is_staff=True, groups__name='RentACarAdministrator')
        return form

class BranchAdmin(admin.ModelAdmin):


    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(BranchAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['rentacar'].queryset = RentACar.objects.filter(id=request.user.rentacaradministrator.rentacarservice_id)
        return form

admin.site.register(RentACar, RentACarAdmin)
admin.site.register(RentACarAdministrator, RentACarAdministratorAdmin)
admin.site.register(Branch, BranchAdmin)