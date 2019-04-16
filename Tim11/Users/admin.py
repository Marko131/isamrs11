from django.contrib import admin
from .models import CustomUser, Request, Friends
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'city', 'phone')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', )}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.readonly_fields = ('is_superuser', 'is_active', 'groups', 'user_permissions', 'last_login', 'date_joined', 'is_staff')
        return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(id=request.user.id)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.is_staff = True
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Request)
admin.site.register(Friends)
