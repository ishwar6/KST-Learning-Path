from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import hashlib
import datetime
import smtplib
import utility_kst
import random

from assessment.models import TestsTaken, User_submission
from states.models import State, Node
from questions.models import Question
from chapters.models import Topic
from userstates.models import TempActiveNode, UserCurrentNode
from itertools import *
import datetime

kstr= None
num_quiz_questions=0
domain_count=0

def index(request):
	global counter, score
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		#print(pr.first_name)
		states=State.objects.all()
		counter=0
		score=0
		return render(request, 'index.html', {'allstates':states, 'profile':user_obj})
	else:
		return redirect('/auth/login/')




def beginquiz(request, chapter_title, state_id):
	if request.user.is_authenticated:
		
		user_obj = User.objects.get(username=request.user)
		global domain_count, kstr, num_quiz_questions

		
		
		if state_id is 'begin':
			chapter= Chapter.objects.get(title= chapter_title)
			test_result=TestsTaken.objects.get_or_create(user=user_obj,chapter=chapter)
			nodes= Nodes.objects.all().filter(state_node__topic___chapter__title= chapter_title)
			kstr= utility_kst.nodes2kstructure(nodes)
			domain_count= utility_kst.num_items_in_domain(kstr)
			num_quiz_questions= utility_kst.number_optimum(domain_count)
			try:
				temp= TempActiveNode.objects.get(user=user_obj, chapter=chapter)
			
			current_knowledge= UserCurrentNode.objects.get_or_create(user=user_obj, chapter=chapter, node=temp.node)
			kfringe_outer= utility_kst.outer_fringe(kstr, current_knowledge.node)
			next_node= random.choice(kfringe_outer)
			successor_state= utility_kst.surplus_state(current_knowledge.node, next_node)
			
			
			
