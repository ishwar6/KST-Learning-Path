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

previous_two_submissions_status = 0 
#previous_two_submissions_status : if last two user submissions are correct value is 2, 
# value is 1 if only last submission is correct, "-1" if ONLY last one was wrong and "-2" if both last two submissions are wrong
# and value 0 if no information present yet

kstr= None
num_quiz_questions=0
domain_count=0
total_questions=0
current_question=0
successor_state=0
iteration=0
end_quiz=0
last_submission=0
last_to_last_submission=0

def index(request):
	global counter, score
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		#print(pr.first_name)
		all_chapters=Chapter.objects.all()
		#print(all_chapters[randint(0, all_chapters.count() - 1)])
		return render(request, 'index.html', {'all_chapters':all_chapters, 'profile':user_obj})
	else:
		return redirect('/auth/login/')




def beginquiz(request, chapter_title, state_id):
	if request.user.is_authenticated:
		
		user_obj = User.objects.get(username=request.user)
		global previous_two_submissions_status,  end_quiz, last_submission, last_to_last_submission
		global domain_count, kstr, num_quiz_questions,total_questions, current_question, successor_state ,iteration
		total_questions=3

		
		
		if state_id == "begin":
			iteration = 1
			chapter= Chapter.objects.get(title= chapter_title)
			#test_result=TestsTaken.objects.get_or_create(user=user_obj,chapter=chapter)
			nodes= Node.objects.all().filter(state_node__topic__chapter= chapter)
			kstr= utility_kst.nodes2kstructure(nodes)
			#domain_count= utility_kst.num_items_in_domain(kstr)
			#num_quiz_questions= utility_kst.number_optimum(domain_count)
			try:
				temp= TempActiveNode.objects.get(user=user_obj, chapter=chapter)
			except:
				print("except TempActiveNode")
			
			# current_knowledge= UserCurrentNode.objects.get_or_create(user=user_obj, chapter=chapter, node=temp.node)
			# kfringe_outer= utility_kst.outer_fringe(kstr, current_knowledge.node)
			# next_node= random.choice(kfringe_outer)
			# successor_state= utility_kst.surplus_state(current_knowledge.node, next_node)			

			successor_state = State.objects.get(title="chap1 topic 1 state 1") #temporarily selecting random state for testing
			all_questions = Question.objects.filter(state=successor_state)
			#print(all_questions)
			current_question = all_questions[randint(0, all_questions.count() - 1)] #selecting a random question from selected state
			#print(current_question)

			context = {
			'firstrun':1,
			'chapter_title':chapter_title,
			'state_id':successor_state.id,
			'currentquestion':current_question
			}

			return render(request, 'quiz.html',context) 



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
		if(iteration == 1 and correct_answer_submission == 1):
			last_to_last_submission = 1
		elif(iteration == 1):
			last_to_last_submission = 0
		elif(iteration == 2 and correct_answer_submission == 1):
			last_submission = 1
		elif(iteration == 2):
			last_submission = 0
		elif(correct_answer_submission == 1):
			last_to_last_submission = last_submission
			last_submission = 1
		else:
			last_to_last_submission = last_submission
			last_submission = 0


		if(iteration>2):
			if(last_submission and last_to_last_submission):
				previous_two_submissions_status = 2
			elif(last_submission):
				previous_two_submissions_status = 1
			elif((not last_submission) and last_to_last_submission):
				previous_two_submissions_status = -1
			elif((not last_submission) and (not last_to_last_submission)):
				previous_two_submissions_status = -2
			else:
				previous_two_submissions_status = 0




		if(previous_two_submissions_status == 2):
			print("do somthing here")
		elif(previous_two_submissions_status == 1):
			print("do somthing here")
		elif(previous_two_submissions_status == 0):
			print("do somthing here")
		elif(previous_two_submissions_status == -1):
			print("do somthing here")
		elif(previous_two_submissions_status == -2):
			print("do somthing here")



		successor_state = State.objects.get(title="chap1 topic 1 state 1") #temporarily selecting random state for testing
		all_questions = Question.objects.filter(state=successor_state)
			#print(all_questions)
		current_question = all_questions[randint(0, all_questions.count() - 1)] #selecting a random question from selected state





		iteration = iteration +1
		print(iteration)

		context = {
		'chapter_title':chapter_title,
		'state_id':successor_state.id,
		'currentquestion':current_question
		}

		return render(request, 'quiz.html',context)






	else:
		return redirect('/auth/login/')
			
			
			
