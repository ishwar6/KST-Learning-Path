from django.conf.urls import url
from .views import IntroductoryResponse
urlpatterns= [
    url(r'^initial',IntroductoryResponse.as_view(), name='initial-assess')
]