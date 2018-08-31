from django.conf.urls import url
from .views import index, beginquiz


urlpatterns = [
    url(r'^main/', index , name='index' ),
    url(r'^beginquiz/(?P<chapter_title>.+)/(?P<state_id>[\w\-\_]+)/', beginquiz , name='beginquiz' ),
]