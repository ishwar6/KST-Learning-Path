# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from chapters.models import Chapter
from django.views.generic import View
from .models import Proficiency, TempActiveNode
from states.models import Node, State

class IntroductoryResponse(View):

    #the_chapters= Chapter.objects.filter(standard=9)
    #print(the_chapters)

    def get(self, request):
        return render(request, 'userstates/initialresponse_form.html', {'chapters': self.the_chapters})

    def post(self, request):
        if Proficiency.objects.filter(user = self.request.user).exists():
            Proficiency.objects.filter(user = self.request.user).delete()
        for the_chapter in self.the_chapters:
            ind_number= "imp-of-"+ str(the_chapter.id)
            ind_select= "level-of-"+ str(the_chapter.id)

            if request.POST.get(ind_select):
                level = request.POST.get(ind_select)
            else:
                level = None
            if request.POST.get(ind_number):
                significance= request.POST.get(ind_number)
            else:
                significance = None
            Proficiency.objects.create(
                user=self.request.user,
                chapter=the_chapter,
                level = level,
                significance = significance

            )
            LEVEL_REF= {
                'beginer':1, 'Benginer':1,
                'intermediate':2, 'Intermediate':2,
                'advanced':3, 'Advanced':3
            }
            nodes= Node.objects.filter(state_node__topic__chapter=the_chapter).distinct()

            num_states_in_domain = 0
            for n in nodes:               
                num_mem= n.state_node.all().count()
                num_states_in_domain= max(num_states_in_domain, num_mem)

            list_of_nodes=[]
            for n in nodes: 
                if n.state_node.all().count() == (num_states_in_domain//4)*LEVEL_REF[level] : #If |Q|=20 node with |Q|/4 = 5 states is assigned to beginer, 10 to interm and so on 
                    list_of_nodes.append(n)
                    print(list_of_nodes)
                    the_node= random.choice(list_of_nodes)

            if TempActiveNode.objects.filter(user = self.request.user).exists():
                TempActiveNode.objects.filter(user = self.request.user).delete()
            
            print("length of list is "+str(len(list_of_nodes)))

            TempActiveNode.objects.create(
                user= self.request.user,
                chapter= the_chapter,
                node= the_node
            )

            '''n = Node.objects.all()
            for chapter in self.the_chapters:
                ind_select= "level-of-"+ str(the_chapter.id)
                level=request.POST.get(ind_select)
                for node in n:
                    print(node.state_node.all().filter(topic__chapter = chapter))
'''
                    #print(node.state_node.all())
                # TempActiveNode.objects.create(
                # user=self.request.user,
                # chapter=chapter,
                # node = node,
                #
                # )
        return render(request, 'userstates/initial_questions.html')
