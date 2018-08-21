from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import hashlib
import datetime
import smtplib

from assessment.models import TestsTaken, User_submission
from chapters.models import Topic, Question
from itertools import *
import datetime
counter=0
score=0
testtken=0
testtime_remaining=""
userinput=list()
getgotousersubmission=0
validitycheck=2

# Create your views here.
def index(request):
	global counter, score
	if request.user.is_authenticated:
		pr = User.objects.get(username=request.user)
		#print(pr.first_name)
		topics=Topic.objects.all()
		counter=0
		score=0
		print(topics)

	#print("counter="+str(counter))

	#print(topics)
		return render(request, 'index.html', {'alltopics':topics, 'profile':pr})
    #return HttpResponse("Hello, world. You're at the main_test index.")
	else:
		return HttpResponse('Some Probem occured')	




def beginquiz(request, choice, qnumber):
	if request.user.is_authenticated:
				pr = User.objects.get(username=request.user)
				#global counter, questions, score, testtken
				global questions, userinput, testtken, testtime_remaining,getgotousersubmission,score,validitycheck
				
				#print("counter="+str(counter))
				
				if qnumber=="begin":
					validitycheck=2
					userinput=list()

					topic=Topic.objects.get(title=choice)
					# if TestsTaken.objects.filter(user=pr, topic=topic):
					# 	return HttpResponse('Sorry '+str(pr.first_name)+' '+ str(pr.last_name)+ ', you have already taken Test!')
					# testtken=TestsTaken.objects.create(user=pr,topic=topic)
					try:
						testtken=TestsTaken.objects.get(user=pr, topic=topic)	
					except:
						testtken=TestsTaken.objects.create(user=pr,topic=topic)
#remove above try except and un-comment the abovve 3 commented lines to let take test once only
					questions=Question.objects.filter(topic=topic)	
					for i in questions:
						try:
							previoususerinput=User_submission.objects.get(user=pr,question=i)
							previoususerinput.delete()
							userinput.append(User_submission.objects.create(user=pr,question=i))
						except:		
							userinput.append(User_submission.objects.create(user=pr,question=i))
						print(userinput)
					return render(request, 'quiz.html',{'questions':questions,'validitycheck':validitycheck, 'topic':topic, 'userinput':userinput, 'firstrun':1,'testtime':topic.total_test_time_in_minutes, 'currentquestion':questions[0]}) 
				testtime_remaining=request.POST.get('timeshow', False)
				if not testtime_remaining:
					testtime_remaining=request.POST.get('timeshow_second', False)

				#print(testtime_remaining)
				print(request.POST.get('validity',False))
				print(request.POST.get('validity2',False))
				
				validitycheck1=int(request.POST.get('validity2',False))
				validitycheck2=int(request.POST.get('validity',False))
				validitycheck=max(validitycheck1, validitycheck2)
				#print(validitycheck1)
				#print(validitycheck2)
				#print(validitycheck)
				#print("validitycheck")

				if request.POST.get('validity',False)=="0" or request.POST.get('validity',False)=="-1":
					return HttpResponse('Sorry '+str(pr.first_name)+' '+ str(pr.last_name)+ ', you have been Disqualified from the Test!')
				if qnumber=="end":
					for i in questions:
						u=User_submission.objects.get(user=pr,question=i)
						if u.op1==i.op1 and u.op2==i.op2 and u.op3==i.op3 and u.op4==i.op4 and u.integer_type_submission==i.integer_type_answer:
							u.correctans=1
							u.save()
							score=score+i.score
					testtken.score=score
					testtken.save()

					return endquiz(request,score,1)
				if request.POST.get('gotoquestion',False)=="1":
					gotoquestionobj=Question.objects.get(id=qnumber)	
					getgotousersubmission=User_submission.objects.get(user=pr,question=gotoquestionobj)
					topic=Topic.objects.get(title=choice)
					return render(request, 'quiz.html',{'questions':questions,'validitycheck':validitycheck, 'topic':topic, 'userinput':userinput, 'firstrun':0,'testtime':testtime_remaining, 'currentquestion':gotoquestionobj, 'getgotousersubmission':getgotousersubmission}) 
#case when user presses submit button
				topic=Topic.objects.get(title=choice)
				total_time_in_string=str(topic.total_test_time_in_minutes)+":00"
				format = '%M:%S'
				#print(ggg)
				gotoquestionobj=Question.objects.get(id=qnumber)
				getgotousersubmission=User_submission.objects.get(user=pr,question=gotoquestionobj)
				getgotousersubmission.op1=0
				getgotousersubmission.op2=0
				getgotousersubmission.op3=0
				getgotousersubmission.op4=0

				startDateTime = datetime.datetime.strptime(total_time_in_string, format)
				endDateTime = datetime.datetime.strptime(testtime_remaining, format)
				diff = startDateTime - endDateTime
				print(diff)

				getgotousersubmission.time_of_sumbission=str(diff)
				getgotousersubmission.submitted_by_user=1
				getgotousersubmission.save()
				

				if request.POST.get('rad', False)=="1":
					getgotousersubmission.op1=1 
				if request.POST.get('rad', False)=="2":
					getgotousersubmission.op2=1 
				if request.POST.get('rad', False)=="3":
					getgotousersubmission.op3=1 
				if request.POST.get('rad', False)=="4":
					getgotousersubmission.op4=1 

				if request.POST.get('one', False)=="1":
					getgotousersubmission.op1=1
				if request.POST.get('two', False)=="1":
					getgotousersubmission.op2=1
				if request.POST.get('three', False)=="1":
					getgotousersubmission.op3=1
				if request.POST.get('four', False)=="1":
					getgotousersubmission.op4=1

				if gotoquestionobj.integer_type:
					#print("beforeLion")
					getgotousersubmission.integer_type_submission=str(request.POST.get('integertype', False))
					#print(userinput.integer_type_submission)
				getgotousersubmission.save()
				for i in userinput:
					if i.question == getgotousersubmission.question:
						i.submitted_by_user=1
				#print(userinput)
				#print("userinput")
				topic=Topic.objects.get(title=choice)
				qq = cycle(questions)
				flag=0
				flag2=0
				for i in qq:
					if flag:
						uu=User_submission.objects.get(user=pr,question=i)
						if flag2:
							nextirrespective = i
							flag2=0
						if uu.submitted_by_user == 0:
							truenext=i
							break
						if i == gotoquestionobj:
							flag = 2
							break

						

					if i == gotoquestionobj:
						flag = 1
						flag2 = 1
				if flag == 2:
					getgotousersubmission=User_submission.objects.get(user=pr,question=nextirrespective)
					return render(request, 'quiz.html',{'questions':questions,'validitycheck':validitycheck, 'topic':topic, 'userinput':userinput, 'firstrun':0,'testtime':testtime_remaining, 'currentquestion':nextirrespective, 'getgotousersubmission':getgotousersubmission})
				else:
					getgotousersubmission=User_submission.objects.get(user=pr,question=truenext)
					return render(request, 'quiz.html',{'questions':questions,'validitycheck':validitycheck, 'topic':topic, 'userinput':userinput, 'firstrun':0,'testtime':testtime_remaining, 'currentquestion':truenext, 'getgotousersubmission':getgotousersubmission})









				
				
				#print(testtime_remaining)

				#print("hello")
				

				


def endquiz(request,score,valid):
	print(score)
	return render(request, 'index.html',{'score':score, 'valid':valid})