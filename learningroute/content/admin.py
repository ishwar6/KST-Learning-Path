from django.contrib import admin

# Register your models here.
from .models import Content, Illustration
admin.site.register(Content)
admin.site.register(Illustration)
