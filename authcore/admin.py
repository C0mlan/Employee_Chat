from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'emp_id', 'role', 'is_staff', 'is_active')
    readonly_fields = ('emp_id',)  # <-- make it read-only

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'emp_id')}),  # include emp_id here
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2')}
        ),
    )

    search_fields = ('email', 'first_name', 'last_name', 'emp_id')
    ordering = ('email',)

admin.site.register(User, UserAdmin)