from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)