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
from random import randint

from assessment.models import TestsTaken, User_submission
from states.models import State, Node
from questions.models import Question
from chapters.models import Topic, Chapter
from userstates.models import TempActiveNode, UserCurrentNode
from itertools import *
import datetime

previous_submissions_status = 0 
#previous_two_submissions_status : if last two user submissions are correct value is 2, 
# value is 1 if only last submission is correct, "-1" if ONLY last one was wrong and "-2" if both last two submissions are wrong
# and value 0 if no information present yet

kstr= 0
num_quiz_questions=0
domain_count=0
chapter=0	


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

curr_knowledge=0
current_question=0
successor_state=0
iteration=0
end_quiz=0

def index(request):
	global counter, score
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		all_chapters=Chapter.objects.all()
		return render(request, 'index.html', {'all_chapters':all_chapters, 'profile':user_obj})
	else:
		return redirect('/auth/login/')




def beginquiz(request, chapter_title, node_id):
	if request.user.is_authenticated:
		
		user_obj = User.objects.get(username=request.user)

		global previous_submissions_status,  end_quiz, curr_knowledge
		global domain_count, kstr, num_quiz_questions, current_question, successor_state ,iteration
		global chapter
		
		
		if node_id == "begin":
			previous_submissions_status=1
			iteration = 0
			chapter= Chapter.objects.get(title= chapter_title)
			nodes= Node.objects.all().filter(state_node__topic__chapter= chapter) #querying out all nodes of chapter in which assessment to be taken
			kstr= utility_kst.nodes2kstructure(nodes) # storing the knowledge structure
			domain_count= utility_kst.num_items_in_domain(kstr) # no of states in domain node(gives us a count of no of steps from {} to Q)
			num_quiz_questions= number_optimum(domain_count) # stores the number of questions of assessment test
			print("the total number of questions is "+str(num_quiz_questions))
			#num_quiz_questions=4
			try:
				temp= TempActiveNode.objects.get(user=user_obj, chapter=chapter)
			except:
				print("except TempActiveNode")
			
			curr_knowledge= UserCurrentNode.objects.get_or_create(user=user_obj, chapter=chapter, node= temp.node)
			next_node= crawl_node(domain_count, previous_submissions_status, temp.node, kstr, chapter)
			


			successor_state = State.objects.get(id= utility_kst.surplus_state(temp.node, next_node)) 
			all_questions = Question.objects.filter(state=successor_state)
			current_question = all_questions[randint(0, all_questions.count() - 1)] #selecting a random question from selected state
			
			context = {
			'firstrun':1,
			'chapter_title':chapter_title,
			'node_id':next_node.id,
			'currentquestion':current_question
			}

			return render(request, 'quiz.html',context) 

		# from hereon the code runs when usersubmission is made.
		crawler_node= Node.objects.get(id=node_id)  # this is the node from which state from which question has just been answered. Quiz is now formally at this node

		op1=0
		op2=0
		op3=0
		op4=0
		integer_type_submission=""

		if request.POST.get('rad', False)=="1":
			op1=1 
		if request.POST.get('rad', False)=="2":
			op2=1 
		if request.POST.get('rad', False)=="3":
			op3=1 
		if request.POST.get('rad', False)=="4":
			op4=1 

		if request.POST.get('one', False)=="1":
			op1=1
		if request.POST.get('two', False)=="1":
			op2=1
		if request.POST.get('three', False)=="1":
			op3=1
		if request.POST.get('four', False)=="1":
			op4=1

		if current_question.integer_type:
			integer_type_submission=str(request.POST.get('integertype', False))

		correct_answer_submission=0
		if op1==current_question.op1 and op2==current_question.op2 and op3==current_question.op3 and op4==current_question.op4 and integer_type_submission==current_question.integeral_answer:
			correct_answer_submission = 1

		

		if correct_answer_submission==1:
			print("KARRACT!!")
			if previous_submissions_status<=0:
				previous_submissions_status=1
			else:
				previous_submissions_status= min(previous_submissions_status+1, 3)
		elif correct_answer_submission==0:
			print("WORNG!!")
			if previous_submissions_status>=0:
				previous_submissions_status=-1
			else:
				previous_submissions_status= max(previous_submissions_status-1, -3)

		iteration = iteration + 1   # iteration holds the number of question already evaluated corresponding to user answer
		
		if(iteration==num_quiz_questions):
			try:
				UserCurrentNode.objects.get(user=user_obj, chapter=chapter).delete()
				UserCurrentNode.objects.create(user=user_obj, chapter=chapter, node=crawler_node)
			except:
				UserCurrentNode.objects.create(user=user_obj, chapter=chapter, node=crawler_node)
			print("NORMAL") ###############################

			return render(request, 'end.html')

		


		next_node= crawl_node(domain_count, previous_submissions_status, crawler_node, kstr, chapter)
		
		
		if next_node == "nothing":
			nl= Node.objects.get_or_create(description='empty')
			try:
				UserCurrentNode.objects.get(user=user_obj, chapter=chapter).delete()
				UserCurrentNode.objects.create(user=user_obj, chapter=chapter, node=nl)
			except:
				UserCurrentNode.objects.create(user=user_obj, chapter=chapter, node=nl)
			print("NOTHING") ###############################
			return render(request, 'end.html')

		
		elif next_node == "everything":
			domain_node= utility_kst.domain_kstate(kstr)
			print("domain node is "+str(domain_node)) ############################################################
			try:
				UserCurrentNode.objects.get(user=user_obj, chapter=chapter).delete()
				UserCurrentNode.objects.create(user=user_obj, chapter=chapter, node=crawler_node)
			except:
				UserCurrentNode.objects.create(user=user_obj, chapter=chapter, node=crawler_node)
			print("EVERYTHING") ###############################

			return render(request, 'end.html')
			
		
		ssid= utility_kst.surplus_state(crawler_node, next_node)
		
		successor_state = State.objects.get(id= ssid)
		all_questions = Question.objects.filter(state=successor_state)
		current_question = all_questions[randint(0, all_questions.count() - 1)] #selecting a random question from selected state

		
		context = {
		'chapter_title':chapter_title,
		'node_id':next_node.id,
		'currentquestion':current_question
		}

		return render(request, 'quiz.html',context)






	else:
		return redirect('/auth/login/')
			
			
		





# This function takes the number of levels of nodes and the no of continuous correct or wrong as i/p and gives the node to be
# crawled to based on previous response if available as o/p

def crawl_node(qlevel, lc, node, kstruct,chapter):
	curr_level= node.state_node.all().count()
	stride=1
	node_crawler= node
	if lc > 0:    #satisfied when current evaluation answer is correct
		'''if lc==1: stride=1
		elif lc==2: stride=3
		elif lc==3: stride=6
		'''
		if curr_level + stride < qlevel:
			for i in range(stride):
				kfringe_outer= utility_kst.outer_fringe(chapter, node)
				node_crawler= random.choice(kfringe_outer)
		else:
			#node_crawler= utility_kst.domain_kstate(kstruct)
			return "everything"
	elif lc < 0:   # satisfied when current evaluated answwr is wrong
		'''if lc==1: stride=1
		elif lc==2: stride=2
		elif lc==3: stride=3
	'''
		if curr_level - stride > 0:
			for i in range(stride):
				kfringe_inner= utility_kst.inner_fringe(chapter, node)
				print("inside crawl node function") #############################
				print(kfringe_inner)
				node_crawler= random.choice(kfringe_inner)
		else:
			return "nothing"

			'''min_node=None
			min_count=qlevel
			for state in node.state_node.all():
				nd= utility_kst.atom(kstruct, state)
				print("*************") ############################
				print(nd)
				if nd.state_node.all().count() < min_count:
					min_node= nd
					min_count= nd.state_node.all().count()
			node_crawler= min_node'''
	return node_crawler

