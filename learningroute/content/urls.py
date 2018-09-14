from django.conf.urls import url
from .views import               (    
                                  showcontent, 
                                  show_list_of_states, 
                                  show_illustrations, 
                                  show_questions, 
                                  assign_new_state,
                                  report,
                                  assignstate,
                                  problem
                                )




urlpatterns= [
    url(r'^assign/newstate/student/change/pwjhfskjdfhkhkd/(?P<id>[0-9]+)/(?P<s>[0-9]+)/$', assignstate,  name='assign'),
    url(r'^learn/state/$', showcontent,  name='show-content'),
    url(r'^problem/sdfd232323sfi3232e232423244nhc234udhd2323e4fuhdsufn2342ed/$', problem,  name='problem'),
    url(r'^list/$', show_list_of_states,  name='list-states'),
    url(r'^illustrations/$', show_illustrations,  name='illustrations'),
    url(r'^questions/$', show_questions,  name='questions'),
    url(r'^assign/new/state/$', assign_new_state,  name='assign'),
    url(r'^report/this/state/$', report,  name='report'),

]
