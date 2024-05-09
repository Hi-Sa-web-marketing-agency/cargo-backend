# cargomanagement/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Enquiry,Notification

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'designation', 'branch']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('designation', 'branch')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'password1', 'password2', 'designation', 'branch')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'designation', 'branch')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Enquiry)
admin.site.register(Notification)
