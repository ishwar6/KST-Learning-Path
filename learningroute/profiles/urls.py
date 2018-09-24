from django.conf.urls import url
from .views import ProfileUpdate

app_name = 'profiles'
urlpatterns = [
    url(r'^edit/$', ProfileUpdate.as_view() , name='edit' ),
    
]
