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
last_correct= 0


def number_optimum(num):
    if num<=20:
        return num//3
    elif num in range(20,30):
        return num//4
    elif num in range(30,50):
        return num//6
    elif num>50 & num<100:
        return num//10
    elif num>100:
        return min(num//15, 30)


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
		global domain_count, kstr, num_quiz_questions, last_correct
		last_correct=1
		
		if state_id is 'begin':
			chapter= Chapter.objects.get(title= chapter_title)
			#test_result=TestsTaken.objects.get_or_create(user=user_obj,chapter=chapter) # not of use for now.
			nodes= Nodes.objects.all().filter(state_node__topic___chapter__title= chapter_title) #querying out all nodes of chapter in which assessment to be taken
			kstr= utility_kst.nodes2kstructure(nodes) # storing the knowledge structure
			domain_count= utility_kst.num_items_in_domain(kstr) # no of states in domain node(gives us a count of no of steps from {} to Q)
			num_quiz_questions= number_optimum(domain_count) # stores the number of questions of assessment test
			try:
				temp= TempActiveNode.objects.get(user=user_obj, chapter=chapter)  #the 'aukaat' of user according to himself/herself(starting node)
			
			current_knowledge= UserCurrentNode.objects.get_or_create(user=user_obj, chapter=chapter, node=temp.node) #variable to hold knowledge of user at every instant
			
			successor_state= utility_kst.surplus_state(current_knowledge.node, next_node) # which state the questtion has to be shown from

			#assuming template rendered here with necessary context data
		


# This function takes the number of levels of nodes and the no of continuous correct or wrong as i/p and gives the node to be
# crawled to based on previous response if available as o/p
def crawl_node(qlevel, lc, node, kstruct):
	curr_level= node.state_node.all().count()
	stride=0
	node_crawler= node

	if lc > 0:
		if lc==1: stride=1
		elif lc==2: stride=3
		elif lc==3: stride=6
		
		if curr_level + stride < lc:
			for i in range(stride):
				kfringe_outer= utility_kst.outer_fringe(kstruct, node)
				node_crawler= random.choice(kfringe_outer)
		else:
			node_crawler= utility_kst.domain_kstate(kstruct)
	
	elif lc < 0:
		if lc==1: stride=1
		elif lc==2: stride=2
		elif lc==3: stride=3
	
		if curr_level + stride < lc:
			for i in range(stride):
				kfringe_inner= utility_kst.inner_fringe(kstruct, node)
				node_crawler= random.choice(kfringe_inner)
		else:
			min_node=None
			min_count=qlevel
			for state in node.state_nodel.all():
				nd= utility_kst.atom(kstruct, state)
				if nd.state_node.all().count() < min_count:
					min_node= nd
					min_count= nd.state_node.all().count()
			node_crawler= min_node

