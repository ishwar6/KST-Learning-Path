from django.conf.urls import url
from .views import showcontent
urlpatterns= [
    url(r'^start', showcontent,  name='start')
]
