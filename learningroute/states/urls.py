from django.conf.urls import url
from .views import myview,  stateadmin, stateedit, selectchapter, selecttopic
app_name = 'states'
urlpatterns = [
    url(r'^$', myview, name ='myview'  ),
    url(r'^admin/$', stateadmin, name='stateadmin'),
   


  
    url(r'^admin/chapter/(?P<title>.+)/', selectchapter , name='selectchapter' ), 
    url(r'^admin/topic/(?P<title>.+)/', selecttopic , name='selecttopic' ), 
    url(r'^admin/(?P<title>.+)/(?P<topic>.+)/', stateedit , name='stateedit' ),
   
   
]
