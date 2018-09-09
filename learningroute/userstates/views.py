# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from chapters.models import Chapter
from django.views.generic import View
from .models import Proficiency, TempActiveNode
from states.models import Node, State
from django.db.models import Q


class IntroductoryResponse(View):
    the_chapters= Chapter.objects.filter(standard=9)

    def get(self, request):
        return render(request, 'userstates/initialresponse_form.html', {'chapters': self.the_chapters})

    def post(self, request):
        for the_chapter in self.the_chapters:
            the_node = None
            if Proficiency.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).exists():
                Proficiency.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).delete()

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
            if nodes is None:
                break
            for n in nodes:
                print('queryset of node is', n)
                num_mem= n.state_node.all().count()
                num_states_in_domain= max(num_states_in_domain, num_mem)
            print('max number of states in CHAPTER_PROFIENCY node', num_states_in_domain)

            list_of_nodes=[]
            a = (num_states_in_domain//4)*LEVEL_REF[level]
            if a==0 & LEVEL_REF[level]==1:
                a = a + 1
            if a==0 & (LEVEL_REF[level]==2 or LEVEL_REF[level]==3):
                a = a+2


            for n in nodes:
                q = n.state_node.all().count()
                print( 'q is ', q , 'and a is', a )
                if q==a or  ( q > a and q < a +  2): #If |Q|=20 node with |Q|/4 = 5 states is assigned to beginer, 10 to interm and so on
                    list_of_nodes.append(n)
                    the_node= random.choice(list_of_nodes)
            if TempActiveNode.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).exists():
                TempActiveNode.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).delete()

            if the_node is not None:

                TempActiveNode.objects.create(
                    user= self.request.user,
                    chapter= the_chapter,
                    node= the_node
                )
        return redirect('/assess/main/', permanent=True)
