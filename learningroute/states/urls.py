from django.conf.urls import url
from .views import myview

urlpatterns = [
   
    url(r'^', myview  )
]
