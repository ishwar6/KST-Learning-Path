from django.conf.urls import url
from .views import myview, nodes

urlpatterns = [

    url(r'^$', myview  ),
    url(r'^nodes$', nodes  )
]
