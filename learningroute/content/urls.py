from django.conf.urls import url
from .views import showcontent, show_list_of_states, show_illustrations, show_questions, assign_new_state
urlpatterns= [
    url(r'^start', showcontent,  name='start'),
    url(r'^list', show_list_of_states,  name='list-states'),
    url(r'^illustrations', show_illustrations,  name='illustrations'),
    url(r'^questions', show_questions,  name='questions'),
    url(r'^assign/new/state', assign_new_state,  name='assign'),

]
