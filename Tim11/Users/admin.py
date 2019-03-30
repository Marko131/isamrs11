from django.contrib import admin
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = ['username', 'email', ]

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

admin.site.register(CustomUser, CustomUserAdmin)