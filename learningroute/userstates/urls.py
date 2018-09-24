from django.urls import re_path as url
from .views import IntroductoryResponse
from .views import first_assessment, assessment_report, start_chapter, active_state

app_name = 'userstates'
urlpatterns= [
    url(r'^initial',IntroductoryResponse.as_view(), name='initial-assess'),
      url(r'^start',first_assessment, name='first'),
    url(r'^report',assessment_report, name='report'),
     url(r'^state/learning/assign/$',start_chapter, name='assign'),

      url(r'^you/$',active_state, name='active'),
]