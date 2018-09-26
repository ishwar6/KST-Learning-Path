from django.contrib import admin

# Register your models here.
from .models import Profile, LoginDetail

admin.site.register(Profile)
admin.site.register(LoginDetail)