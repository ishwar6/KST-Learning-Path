from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import  static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^states/', include('states.urls')),
    url(r'^auth/', include('authentication.urls')),
    url(r'^assess/', include('assessment.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)