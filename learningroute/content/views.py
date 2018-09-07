from django.shortcuts import render
from django.db.models import Q, Count
from chapters.models import Chapter
from userstates.models import UserCurrentNode, TempActiveNode
from states.models import State, Node
from content.models import Content, Illustration, IllustrationGiven
# Create your views here.
import utility_kst as u

def showcontent(request):
    user = request.user
    chapter = Chapter.objects.filter(title__contains = 'number').first()


    if chapter is not None:
        user_active_node       = TempActiveNode.objects.filter(Q(user = user) & Q(chapter = chapter)).first().node
        user_active_node_list  = str(user_active_node).split(',')
        current_chapter_nodes  = Node.objects.annotate(Count('state_node')).filter(state_node__topic__chapter = chapter)
        current_chapter_state  = State.objects.filter(topic__chapter = chapter)
        num_states_in_domain   = 0
        user_next_node         = u.outer_fringe(chapter, user_active_node)
        if len(user_next_node) == 0 :
            print('Nothing left in this chapter')
            context = {'empty' : True}
            return render(request, 'content/page.html', context )

        user_next_node         = user_next_node[0].state_node.all()


        node_list = []

        for node in user_next_node:
            node_list.append(node.title)
        current_node_set      = set(node_list) - set(user_active_node_list)
        current_node          = next(iter(current_node_set))






        topic_to_learn = Content.objects.filter(state__title = current_node).first()

        illustrations  = Illustration.objects.filter(content = topic_to_learn)

        illustration_given  = IllustrationGiven.objects.all()






        context = {
          'q'       : user_active_node_list,
          'current' : current_node,
          'state'   : current_chapter_state,
          'node'    : current_chapter_nodes,
          'chapter' : user_next_node,
          'topic'   : topic_to_learn,
          'empty'   : False,
          'illust'  : illustrations,
        }
    return render(request, 'content/page.html', context )
