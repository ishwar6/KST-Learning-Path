# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from chapters.models import Chapter
from django.views.generic import View
from .models import Proficiency, TempActiveNode
from states.models import Node

class IntroductoryResponse(View):

    the_chapters= Chapter.objects.filter(standard=9)
    print(the_chapters)

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
