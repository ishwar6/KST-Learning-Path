from django.conf.urls import url
from .views import InitialresponseCreate

urlpatterns= [
    url(r'^initial',InitialresponseCreate.as_view(), name='initial-assess')
]