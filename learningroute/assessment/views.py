from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import hashlib
import datetime
import smtplib

from assessment.models import TestsTaken, User_submission
from states.models import State
from questions.models import Question
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




def beginquiz(request, state_title, qnumber):
	if request.user.is_authenticated:
				user_obj = User.objects.get(username=request.user)
				global questions, store_users_submission, test_result, testtime_remaining,question_submission,score,total_time_in_string


				if qnumber=="begin": #When the quiz starts for the first time	
					store_users_submission=list()
					state=State.objects.get(title=state_title) #select state chosen by user
					try:
						test_result=TestsTaken.objects.get(user=user_obj, state=state)   #To store user's test results
					except:
						test_result=TestsTaken.objects.create(user=user_obj,state=state)

					questions=Question.objects.filter(state=state) 
					for i in questions:
						try:       #User_submission stores user's submission and time for each question in a state, if the user
								   # had already given the test, we need to delete them and create new empty objects to store the 
								   # user_submissions for  each questions of this test
							old_user_submission=User_submission.objects.get(user=user_obj,question=i)
							old_user_submission.delete()
							store_users_submission.append(User_submission.objects.create(user=user_obj,question=i))
						except:
							store_users_submission.append(User_submission.objects.create(user=user_obj,question=i))
						


					context = {'questions':questions,
									'state':state,
									'store_users_submission':store_users_submission,
									 'testtime':state.time,
									 'firstrun':1,                      #to set timer properly for the first run                
									  'currentquestion':questions[0]   #by default displaying the 1st question for first time
									 }


					return render(request, 'quiz.html', context)

                    # Below 'timeshow' and 'timeshow_second' both have the same value, but since there are 2 forms in the page, 
                    # one when user switches between  questions and another where user submits an answer, the time value needs
                    # to be sent through both the forms so time can be updated properly. 

				if request.method == 'POST':
					testtime_remaining=request.POST.get('timeshow', False)

					if not testtime_remaining:
						testtime_remaining=request.POST.get('timeshow_second', False)

				
				if qnumber=="end":   #when user clicks end_quiz we check the user's submissions from the actual answers for the questions
					for i in questions:
						u=User_submission.objects.get(user=user_obj,question=i)
						if u.op1==i.op1 and u.op2==i.op2 and u.op3==i.op3 and u.op4==i.op4 and u.integer_type_submission==i.integeral_answer:
							u.correctans=1
							u.save()
							score=score+i.score
					test_result.score=score
					test_result.save()
					return endquiz(request,score,1)

				if request.POST.get('gotoquestion',False)=="1": #goto_user_question is the question to which the user wants to go to 
					goto_user_question=Question.objects.get(id=qnumber)
					question_submission=User_submission.objects.get(user=user_obj,question=goto_user_question)
					state=State.objects.get(title=state_title)

					context = {'questions':questions, 
					'state':state, 
					'store_users_submission':store_users_submission, 
					'firstrun':0,'testtime':testtime_remaining, 
					'currentquestion':goto_user_question, 
					'question_submission':question_submission}

					return render(request, 'quiz.html',context)
#case when user presses submit button for the current quiz question
#question_submission is used to store the response of the user's submission for the currently submitted question
				state=State.objects.get(title=state_title)
				total_time_in_string=str(state.time)+":00"
				format = '%M:%S'
				#print(ggg)
				current_question=Question.objects.get(id=qnumber)
				question_submission=User_submission.objects.get(user=user_obj,question=current_question)
				question_submission.op1=0
				question_submission.op2=0
				question_submission.op3=0
				question_submission.op4=0

				startDateTime = datetime.datetime.strptime(total_time_in_string, format)
				endDateTime = datetime.datetime.strptime(testtime_remaining, format)
				time_difference = startDateTime - endDateTime
				# print(time_difference)

				question_submission.time_of_sumbission=str(time_difference)
				question_submission.submitted_by_user=1
				question_submission.save()


				if request.POST.get('rad', False)=="1":
					question_submission.op1=1
				if request.POST.get('rad', False)=="2":
					question_submission.op2=1
				if request.POST.get('rad', False)=="3":
					question_submission.op3=1
				if request.POST.get('rad', False)=="4":
					question_submission.op4=1

				if request.POST.get('one', False)=="1":
					question_submission.op1=1
				if request.POST.get('two', False)=="1":
					question_submission.op2=1
				if request.POST.get('three', False)=="1":
					question_submission.op3=1
				if request.POST.get('four', False)=="1":
					question_submission.op4=1

				if current_question.integer_type:
					
					question_submission.integer_type_submission=str(request.POST.get('integertype', False))
					
				question_submission.save()
				for i in store_users_submission:
					if i.question == question_submission.question:
						i.submitted_by_user=1
				
				state=State.objects.get(title=state_title)


				#below algorithm is used to cyclically obtain the next question for displaying to the user as 
				# the user needs to be shown the next un-attempted question

				qq = cycle(questions)
				flag=0
				flag2=0
				for i in qq:
					if flag:
						uu=User_submission.objects.get(user=user_obj,question=i)
						if flag2:
							nextirrespective = i
							flag2=0
						if uu.submitted_by_user == 0:
							truenext=i
							break
						if i == current_question:
							flag = 2
							break
					if i == current_question:
						flag = 1
						flag2 = 1
				if flag == 2:
					question_submission=User_submission.objects.get(user=user_obj,question=nextirrespective)
					return render(request, 'quiz.html',{'questions':questions, 'state':state, 'store_users_submission':store_users_submission, 'firstrun':0,'testtime':testtime_remaining, 'currentquestion':nextirrespective, 'question_submission':question_submission})
				else:
					question_submission=User_submission.objects.get(user=user_obj,question=truenext)
					return render(request, 'quiz.html',{'questions':questions, 'state':state, 'store_users_submission':store_users_submission, 'firstrun':0,'testtime':testtime_remaining, 'currentquestion':truenext, 'question_submission':question_submission})
	else:
		return redirect('/auth/login/')



def endquiz(request,score,valid):
	if request.user.is_authenticated:
		print(score)
		return render(request, 'index.html',{'score':score, 'valid':valid})
	else:
		return redirect('/auth/login/')
	
