from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/', views.index  ),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),

]