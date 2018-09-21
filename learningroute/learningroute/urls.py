from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import  static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^myaccount/', include('accounts.urls', namespace='account')),
    url(r'^states/', include('states.urls',namespace='states')),
    url(r'^auth/', include('authentication.urls')),
    url(r'^userstates/', include('userstates.urls', namespace='userstates')),
    url(r'^assess/', include('assessment.urls', namespace='assess')),
    url(r'^chapters/', include('chapters.urls', namespace='chapters')),
    url(r'^content/', include('content.urls', namespace='content'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
