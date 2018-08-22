from django.conf.urls import url
from .views import myview, nodes, stateadmin, stateedit, selectchapter, selecttopic, nodeadmin, nodeedit, addnode, edgeadmin, edgeedit, addedge

urlpatterns = [
    url(r'^$', myview  ),
    url(r'^admin/$', stateadmin),
    url(r'^admin/node/$', nodeadmin , name='nodeadmin' ), 
    url(r'^admin/edge/$', edgeadmin , name='edgeadmin' ), 

    url(r'^admin/node/(?P<nodeid>(\d+))/', nodeedit , name='nodeedit' ),
    url(r'^admin/edge/(?P<edgeid>(\d+))/', edgeedit , name='edgeedit' ), 
    url(r'^admin/addedge/(?P<chapid>(\d+))/', addedge , name='addedge' ),

    url(r'^admin/addnode/(?P<chapid>(\d+))/', addnode , name='addnode' ), 
    url(r'^admin/chapter/(?P<title>.+)/', selectchapter , name='selectchapter' ), 
    url(r'^admin/topic/(?P<title>.+)/', selecttopic , name='selecttopic' ), 
    url(r'^admin/(?P<title>.+)/(?P<topic>.+)/', stateedit , name='stateedit' ),
   
    url(r'^nodes$', nodes  )
]
