from django.contrib import admin

# Register your models here.
from .models import Content, Illustration, IllustrationGiven
admin.site.register(Content)
admin.site.register(Illustration)
admin.site.register(IllustrationGiven)