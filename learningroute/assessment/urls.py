from django.conf.urls import url
from .views import first_assessment, assessment_report, start_chapter, active_state

app_name= 'assessment' #useful for namespaceing of urls of a specific app 

urlpatterns = [
 


    url(r'^start',first_assessment, name='first'),
    url(r'^report',assessment_report, name='report'),
     url(r'^state/learning/assign/$',start_chapter, name='assign'),

      url(r'^you/$',active_state, name='active'),
    
]


