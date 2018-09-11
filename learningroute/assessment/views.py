from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import hashlib
import datetime
import smtplib
import utility_kst
from random import choice
from random import randint

from django.contrib import messages
from assessment.models import TestsTaken, User_submission
from states.models import State, Node
from questions.models import Question
from chapters.models import Topic, Chapter
from userstates.models import TempActiveNode, UserCurrentNode, Proficiency
from django.db.models import Q
from itertools import *
import datetime

previous_submissions_status = 0
'''previous_two_submissions_status : if last two user submissions are correct value is 2,
value is 1 if only last submission is correct, "-1" if ONLY last one was wrong and "-2" if both last two submissions are wrong
 and value 0 if no information present yet'''

kstr= 0
num_quiz_questions=0
domain_count=0
chapter=0
qset_chapters= Chapter.objects.filter(standard=11)
curr_knowledge=0
current_question=0
successor_state=0
iteration=0
index_next_chapter=0
end_quiz=0

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
		all_chapters=Chapter.objects.filter(standard=11)
		try:
			return render(request, 'index.html', {'first_chapter':all_chapters[0], 'profile':user_obj})
		except:
			return render(request, 'index.html', {'first_chapter':all_chapters, 'profile':user_obj})

	else:
		return redirect('/auth/login/')

# fr stands for first_run in arguments
# helper function for assigning glob-vars with appropriate values before quiz from a new chapter begins
def beginquiz(request, user_obj, chapter_from_url, fr):

	global previous_submissions_status,  end_quiz, curr_knowledge
	global domain_count, kstr, num_quiz_questions, current_question, successor_state ,iteration
	global chapter, qset_chaters
	global index_next_chapter
	previous_submissions_status=1

	iteration = 0

	index_next_chapter= index_next_chapter + 1
	chapter_from_url= Chapter.objects.get(title= chapter_from_url)
	chapter= Chapter.objects.get(title=chapter_from_url)
	print(" quiz on : ",chapter.title)
	nodes= Node.objects.all().filter(state_node__topic__chapter= chapter_from_url) #querying out all nodes of chapter in which assessment to be taken
	if nodes.count()==0:
		return 1
	# storing the knowledge structure
	#print(nodes)
	kstr= utility_kst.nodes2kstructure(nodes)

	#print(kstr)
	# no of states in domain node(gives us a count of no of steps from {} to Q)
	domain_count= utility_kst.num_items_in_domain(kstr)

	print('domain count is', domain_count)
 # stores the number of questions of assessment test while making sure that number of node levels is not too small than we can work with

 #number_optimal returns number of questions to be asked in assessment on the basis of domain count
	num_quiz_questions= number_optimum(domain_count)  

	# num_quiz_questions would be zero if n(States in chapter) < 4 Avoid that from happening even during testing 

	if num_quiz_questions==0:                           
		messages.error(request, 'Number of states in chapter is too less. Not even permissible in development env ')
		return 1

	print("the total number of questions is "+str(num_quiz_questions))##########################################
	#num_quiz_questions=4

	temp= TempActiveNode.objects.get(user=user_obj, chapter=chapter_from_url)
	if not temp:
		messages.error(request, 'the temporary knowledge state of user has not been collected from previous introcudtory response step. Please proceed again')
		return render(request, 'mdisplay.html')



	next_node=None
	successor_state=None


	if temp.dont_know_switch:            # if the user has selected that he doesnt know chapter then he knows nothing
		
		# to get all the nodes with 1 state in them
		unity_nodes= []
		for nd in nodes:
			if nd.state_node.all().count()==1:
				unity_nodes.append(nd)
		next_node= choice(unity_nodes)
		
		first_question_state= [st for st in next_node.state_node.all()]
		successor_state= first_question_state[0]

	
	else:     # if user has selected proficency other than 'dont know' then node is called from temp active node

		#going to crawl_node function 
		#####################________________________________CRAWL NODE_______________________________________####################

		next_node= crawl_node(domain_count, previous_submissions_status, temp.node, kstr, chapter_from_url)

		#####################________________________________CRAWL NODE DONE_______________________________________####################

		if next_node is None:
			messages.error(request, 'next node to be traversed couldnt be obtained. Check utility code and aux functions')
			return render(request, 'mdisplay.html')

		successor_state = State.objects.get(id= utility_kst.surplus_state(temp.node, next_node))



	print("starting with this state :", successor_state)
	# at this point we have the dest node and also the state from which question to be given.
	try:
		all_questions = Question.objects.filter(state=successor_state)
		if not all_questions:
			messages.error(request, 'Question with given state', successor_state, 'not found')
			return render(request, 'mdisplay.html')
		print(all_questions)
	except:
		messages.error(request, 'error retreiving Question with given state', successor_state)			



 #selecting a random question from selected state

	current_question = all_questions[randint(0, all_questions.count() - 1)]


	context = {
		'firstrun':fr,
		'chapter_title':chapter_from_url,
		'node_id':next_node.id,
		'currentquestion':current_question
	}
	print(context)
	return context



def quiz(request, chapter_title, node_id):
	if request.user.is_authenticated:

		usr = User.objects.get(username=request.user)

		global previous_submissions_status,  end_quiz, curr_knowledge
		global domain_count, kstr, num_quiz_questions, current_question, successor_state ,iteration
		global chapter, qset_chaters
		global index_next_chapter


		#############################################  FIRST QUESTION TURN   ################

		if node_id == "begin":
			index_next_chapter=0
			print(chapter_title)
			#first_run =1 
			context = beginquiz(request, usr, chapter_title, 1)
			print(context)
			
			# Iterate over all of the other chapters while context is one
			# qset_chapters is a queryset that returns chapters whith given standard; declared in above variables
			#In case kstructure is not in a chapter
			while(context==1):
				context = beginquiz(request, usr, qset_chapters[index_next_chapter].title, 0)
			return render(request, 'quiz.html',context)



			# from hereon the code runs when usersubmission is made.


		
		# this is the node from which state from which question has just been answered. 
		# Quiz is now formally at this node
		crawler_node= Node.objects.get(id=node_id)  

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



#setting previous_submissions_status 1,2,-1,-2 or 0 on the basis of current and previous_status values

		if correct_answer_submission==1:

			print("Correct!!")

			if previous_submissions_status<=0:
				previous_submissions_status=1

			else:
				previous_submissions_status= min(previous_submissions_status+1, 3)

		elif correct_answer_submission==0:

			print("Wrong!!")

			if previous_submissions_status>=0:
				previous_submissions_status=-1
			else:
				previous_submissions_status= max(previous_submissions_status-1, -3)

# iteration holds the number of question already evaluated corresponding to user answer
		iteration = iteration + 1   

		if(iteration==num_quiz_questions):

			if UserCurrentNode.objects.filter(user=usr, chapter=chapter).exists():
				UserCurrentNode.objects.filter(user=usr, chapter=chapter).delete()

			UserCurrentNode.objects.create(user=usr, chapter=chapter, node=crawler_node)

			print("NORMAL")
	 ###############################

			try:
				next_chapter= qset_chapters[index_next_chapter]
				context= beginquiz(request, usr, next_chapter.title,0)

				while(context==1):
					context= beginquiz(request, usr, qset_chapters[index_next_chapter].title,0)

				return render(request, 'quiz.html', context)

			except:
				return render(request, 'end.html')




		next_node= crawl_node(domain_count, previous_submissions_status, crawler_node, kstr, chapter_title)


		if next_node == "nothing":
			nl= Node.objects.get_or_create(description='empty')
			if UserCurrentNode.objects.filter(user=usr, chapter=chapter).exists():
				UserCurrentNode.objects.filter(user=usr, chapter=chapter).delete()
			UserCurrentNode.objects.create(user=usr, chapter=chapter, node=nl)
			print("NOTHING") ###############################

			try:
				next_chapter= qset_chapters[index_next_chapter]
				context= beginquiz(request, usr, next_chapter.title, 0)
				while(context==1):
					context= beginquiz(request, usr, qset_chapters[index_next_chapter].title,0)
				return render(request, 'quiz.html', context)
			except:
				return render(request, 'end.html')


		elif next_node == "everything":
			domain_node= utility_kst.domain_kstate(kstr)
			print("domain node is "+str(domain_node)) ############################################################

			if UserCurrentNode.objects.filter(user=usr, chapter=chapter).exists():
				UserCurrentNode.objects.filter(user=usr, chapter=chapter).delete()
			UserCurrentNode.objects.create(user=usr, chapter=chapter, node=crawler_node)
			print("EVERYTHING") ###############################

			try:
				next_chapter= qset_chapters[index_next_chapter]
				context= beginquiz(request, usr, next_chapter.title,0)
				while(context==1):
					context= beginquiz(request ,usr, qset_chapters[index_next_chapter].title)
				return render(request, 'quiz.html', context)
			except:
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








# This function takes the number of levels of nodes and 
# the no of continuous correct or wrong as i/p and gives the node to be
# crawled to based on previous response if available as o/p

#lc is previous_submission_status
#qlevel is domain_count
def crawl_node(qlevel, lc, node, kstruct, chapter):
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
				node_crawler= choice(kfringe_outer)
		else:
			#node_crawler= utility_kst.domain_kstate(kstruct)
			return "everything"
	elif lc < 0:   # satisfied when current evaluated answer is wrong
		'''if lc==1: stride=1
		elif lc==2: stride=2
		elif lc==3: stride=3
	'''
		if curr_level - stride > 0:
			for i in range(stride):
				kfringe_inner= utility_kst.inner_fringe(chapter, node)
				print("inside crawl node function") #############################
				print(kfringe_inner)
				node_crawler= choice(kfringe_inner)
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



class IntroductoryResponse(View):
	the_chapters= Chapter.objects.filter(standard=11)

	def get(self, request):
		return render(request, 'userstates/initialresponse_form.html', {'chapters': self.the_chapters})
	
	def post(self, request):
		LEVEL_REF={
			'beginer':1,
			'Benginer':1,
			'intermediate':2,
			'Intermediate':2,
			'advanced':3,
			'Advanced':3,
			'dont know':0,
			'Dont Know':0
			}
		for the_chapter in self.the_chapters :
			the_node = None
			if Proficiency.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).exists():
				Proficiency.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).delete()

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

			dont_know_var = False
		
			if LEVEL_REF[level]== 0:
				dont_know_var=True
			else:	
				nodes= Node.objects.filter(state_node__topic__chapter=the_chapter).distinct()

				num_states_in_domain = 0
				if nodes is None:
					break
				for n in nodes:
					print('queryset of node is', n)
					num_mem= n.state_node.all().count()
					num_states_in_domain= max(num_states_in_domain, num_mem)
				print('max number of states in CHAPTER_PROFIENCY node', num_states_in_domain)

				list_of_nodes=[]
				a = (num_states_in_domain//4)*LEVEL_REF[level]
				if a==0 & LEVEL_REF[level]==1:
					a = a + 1
				if a==0 & (LEVEL_REF[level]==2 or LEVEL_REF[level]==3):
					a = a+2

				for n in nodes:
					q = n.state_node.all().count()
					print( 'q is ', q , 'and a is', a )
					if q==a or  ( q > a and q < a +  2): #If |Q|=20 node with |Q|/4 = 5 states is assigned to beginer, 10 to interm and so on
						list_of_nodes.append(n)
						the_node= choice(list_of_nodes)
			
			Proficiency.objects.create(
				user=self.request.user,
				chapter=the_chapter,
				level = level,
				significance = significance,
				dont_know_switch= dont_know_var
			)
			if TempActiveNode.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).exists():
				TempActiveNode.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).delete()

			TempActiveNode.objects.create(
				user= self.request.user,
				chapter= the_chapter,
				node= the_node,
				dont_know_switch= dont_know_var
			)
		
		return redirect('assessment:index')



def endview(request):
	return render(request, 'mdisplay.html', {})