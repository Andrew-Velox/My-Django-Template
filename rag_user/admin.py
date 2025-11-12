from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {'fields': ('image',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {'fields': ('image',)}),
    )



admin.site.register(CustomUser, CustomUserAdmin)