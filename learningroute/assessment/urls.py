from django.conf.urls import url
from .views import index, quiz, IntroductoryResponse, endview

app_name= 'assessment' #useful for namespaceing of urls of a specific app 

urlpatterns = [
    url(r'^main/', index , name='index' ),
    url(r'^quiz/(?P<chapter_title>.+)/(?P<node_id>[\w\-\_]+)/', quiz , name='quiz' ),
    url(r'^initial',IntroductoryResponse.as_view(), name='initial-assess'),
    url(r'^ends',endview, name='end'),
    
]


