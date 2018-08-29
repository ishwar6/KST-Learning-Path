from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import hashlib
import datetime
import smtplib
import utility_kst

from assessment.models import TestsTaken, User_submission
from states.models import State, Node
from questions.models import Question
from chapters.models import Topic
from userstates.models import TempActiveNode, UserCurrentNode
from itertools import *
import datetime
counter=0
score=0
test_result=0
testtime_remaining=""
total_time_in_string=0
store_users_submission=list()
question_submission=0



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
		global questions, store_users_submission, test_result, testtime_remaining,question_submission,score,total_time_in_string

		chapter= Chapter.objects.get(title= chapter_title)
		test_result=TestsTaken.objects.get_or_create(user=user_obj,chapter=chapter)
		nodes= Nodes.objects.all().filter(state_node__topic___chapter__title= chapter_title)
		kstr= utility_kst.nodes2kstructure(nodes)
		
		if state_id is 'begin':
			try:
				temp= TempActiveNode.objects.get(user=user_obj, chapter=chapter)
			current_knowledge= 

			
