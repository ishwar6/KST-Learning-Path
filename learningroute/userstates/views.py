# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from chapters.models import Chapter
from django.views.generic import View
from .models import Proficiency


class IntroductoryResponse(View):

    the_chapters= Chapter.objects.filter(standard=9)
    print(the_chapters)

    def get(self, request):
        return render(request, 'userstates/initialresponse_form.html', {'chapters': self.the_chapters})

    def post(self, request):
        for the_chapter in self.the_chapters:
            ind_number= "imp-of-"+ str(the_chapter.id)
            ind_select= "level-of-"+ str(the_chapter.id)
            Proficiency.objects.create(
                user=self.request.user,
                chapter=the_chapter,
                level=request.POST.get(ind_select),
                significance= request.POST.get(ind_number)
            )
        return render(request, 'userstates/initial_questions.html')
