from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^states/', include('states.urls')),
    url(r'^auth/', include('authentication.urls'))
]
