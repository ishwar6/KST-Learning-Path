from django.urls import re_path as url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import  static
from accounts.views import LoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', LoginView.as_view()),
    url(r'^myaccount/', include('accounts.urls', namespace='account')),
    url(r'^states/', include('states.urls',namespace='states')),

    url(r'^userstates/', include('userstates.urls', namespace='assess')),

    url(r'^chapters/', include('chapters.urls', namespace='chapters')),
    url(r'^content/', include('content.urls', namespace='content')),

     url(r'^profile/', include('profiles.urls', namespace='profile'))
]



if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)