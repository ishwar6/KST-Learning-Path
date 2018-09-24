from django.conf.urls import url
from .views import mainpage, editchapter, edittopic #, nodes, stateadmin, stateedit, selectchapter, selecttopic
app_name = 'chapters'
urlpatterns = [
    url(r'^$', mainpage , name='mainpage' ),
    url(r'^(?P<chapternumber>(\d+))/', editchapter , name='editchapter' ),
    url(r'^topic/(?P<topicnumber>(\d+))/', edittopic , name='edittopic' ),
    # url(r'^admin/$', stateadmin),
    # url(r'^admin/chapter/(?P<title>.+)/', selectchapter , name='selectchapter' ), 
    # url(r'^admin/topic/(?P<title>.+)/', selecttopic , name='selecttopic' ), 
    # url(r'^admin/(?P<title>.+)/(?P<topic>.+)/', stateedit , name='stateedit' ),
    # url(r'^nodes$', nodes  )
]
