# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from .models import Initialresponse
from django.views.generic.edit import CreateView

# Create your views here.
class InitialresponseCreate(CreateView):
    model= Initialresponse
    fields='__all__'
    
    def post(self, request):
        return render(request, 'userstates/initial_questions.html')