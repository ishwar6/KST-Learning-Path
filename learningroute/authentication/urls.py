from django.conf.urls import url
from .views import login, logout


urlpatterns = [
    url(r'^login/', login),
    url(r'^logout/', logout),

]