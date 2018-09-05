from django.conf.urls import url
from .views import index, beginquiz, IntroductoryResponse

urlpatterns = [
    url(r'^main/', index , name='index' ),
    url(r'^beginquiz/(?P<chapter_title>.+)/(?P<node_id>[\w\-\_]+)/', beginquiz , name='beginquiz' ),
    url(r'^initial',IntroductoryResponse.as_view(), name='initial-assess'),
]