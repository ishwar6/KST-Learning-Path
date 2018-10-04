from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from states.models import State, Node
from questions.models import Question
from chapters.models import Topic, Chapter
from userstates.models import TempActiveNode, PracticeChapter, UserState	
from content.models import CurrentActiveNode, CurrentActiveState
from django.db.models import Q


import utility_kst
import random 
User = get_user_model()





class IntroductoryResponse(View):
	

	def get(self, request):
		if not self.request.user.is_authenticated:
			return redirect('account:login')
		else:

			standard    = self.request.user.standard
			the_chapters= Chapter.objects.filter(standard=standard)
			student_state_ = UserState.objects.filter(user = self.request.user)
			if student_state_.exists():
				student_state = student_state_.first()
				print('s', student_state.active_part)
				if student_state.active_part != 0:
					return redirect('assess:active')
			return render(request, 'userstates/initialresponse_form.html', {'chapters': the_chapters})
		
	def post(self, request):
		if not self.request.user.is_authenticated:
			return redirect('account:login')
		else:
			standard    = self.request.user.standard
			the_chapters= Chapter.objects.filter(standard=standard)
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
			for the_chapter in the_chapters :
				the_node = None
				ind_select= "level-of-"+ str(the_chapter.id)

				if request.POST.get(ind_select):
					level = request.POST.get(ind_select)
				else:
					level = None
				

				dont_know_var = False
			
				if LEVEL_REF[level]== 0:
					dont_know_var=True
				else:	
					nodes= Node.objects.filter(state_node__topic__chapter=the_chapter).distinct()
					print(nodes)


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
							print('ACTIVE NODE HERE IS' , n)
							list_of_nodes.append(n)
					the_node= random.choice(list_of_nodes)
					print(list_of_nodes)
					print(the_node	)
				
				
				if TempActiveNode.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).exists():
					TempActiveNode.objects.filter(Q(user = self.request.user) & Q(chapter = the_chapter)).delete()

				TempActiveNode.objects.create(
					user= self.request.user,
					chapter= the_chapter,
					node= the_node,
					dont_know_switch= dont_know_var
				)	
			

			student_state_ = UserState.objects.filter(user = self.request.user)
			if student_state_.exists():
				student_state = student_state_.first()
				student_state.active_part = 1
				student_state.save()
			return redirect('assess:first')




def number_optimum(num):
	if num<=20:
		return num//3
	elif num in range(20,30):
		return num//4
	elif num in range(30,50):
		return num//5
	elif num>50 & num<100:
		return num//6
	elif num>100:
		return min(num//15, 30)



def change_temp_state(request, chapter, new_node ):
	''' It takes chapter for which new_node is to be updated in TempActiveNode
	 for a particular request.user'''

	user          = request.user
	previous_node = TempActiveNode.objects.filter( Q(user = user) & Q(chapter = chapter))
	if previous_node.exists():
		print('deleting previous node incorrect')
		previous_node.delete()
	


	TempActiveNode.objects.create(
		user 	= user,
		chapter = chapter_for_assessment[0],
		node 	= new_node
		)
	print('new node created for chapter')

	return True




def first_assessment(request):
	user = request.user
	global correct, incorrect, question_to_render, current_question, temp_states
	global number_of_question 
	number_of_question = 0
	#context = {}
	global chapter_for_assessment 

	if user.is_authenticated:
		if request.method == 'GET':
			standard       = user.standard

			student_state_ = UserState.objects.filter(user = user)
			if student_state_.exists():
				student_state = student_state_.first()
				if student_state.active_part!=1:
					return redirect('assess:active')


			correct = incorrect = 0
			temp_states = TempActiveNode.objects.filter(user = user)
			chapters    = Chapter.objects.filter(standard = standard)
			chapter_for_assessment = []

			for c in chapters:
				temp_state = temp_states.filter(chapter = c)
				print('this state is - -- - ', temp_state, 'for chapter - - - - ', c)
				if temp_state.exists():
					dont_know = temp_state.first().dont_know_switch
					node      = temp_state.first().node
					if dont_know is True or node is None :
						print('Dont know chapter, move to next chapter')
						continue
					else:
						chapter_for_assessment.append(c)
			a = 1
			print('all list of chapter_for_assessment are', chapter_for_assessment)
			
			while( len(chapter_for_assessment) != 0 ):
				print('assessment chapter here is ', a)
				chapter_for_assessment = random.sample(chapter_for_assessment, len(chapter_for_assessment))  
				question, current_node             = choose_question(request, temp_states, chapter_for_assessment, 1)
				a = a+1
				print('This question is', question)

				if question is None:
					print('question was none, shorting the list by one')
					if len(chapter_for_assessment)==0:
						break
					else:
						chapter_for_assessment = chapter_for_assessment[1::1]
				else:
					break
					
					
				

			print( 'very FIRST chapter of assessment here in get is',  chapter_for_assessment)
			current_question = question.last()
			

			context = {
						'currentquestion' : current_question,
					}
			return render(request, 'userstates/assement_ques.html', context)

		if request.method == 'POST':
			number_of_question = number_of_question + 1
			print('current_question is', current_question)
			print('here chapter of assessment',  chapter_for_assessment)
			op1 = op2 =  op3 =  op4 = 0
			integer_type_submission=""
			this_q = 0
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
				print('answer submitted is', integer_type_submission)
			correct_answer_submission=0
			if op1==current_question.op1 and op2==current_question.op2 and op3==current_question.op3 and op4==current_question.op4 and integer_type_submission==current_question.integeral_answer:
				correct_answer_submission = 1

			

			
			if len(chapter_for_assessment) ==0:
				print('chapter ends! Done')
				return redirect('content:problem') 
			chapter = chapter_for_assessment[0]
			
			
			
				

			if correct_answer_submission==1:
				print('here number of question is', number_of_question)
				
				correct = correct + 1
				this_q = 1
				message = ' Correct Answer, Nice!! '
				(question, current_node) = choose_question(request, temp_states, chapter_for_assessment, 1)
				if question is None or number_of_question > 5:
					print('this time node is', current_node)

					if len(chapter_for_assessment) == 0:
							print("Quiz ends")
							student_state_ = UserState.objects.filter(user = user)
							if student_state_.exists():
								student_state = student_state_.first()
								student_state.active_part = 2
								student_state.save()
							return JsonResponse({'empty' : True})
					change_temp_state(request, chapter_for_assessment[0], current_node)
					number_of_question  = 0

					print('New node created for', chapter_for_assessment[0])
					# assessment for this chapter is done: Move to next chapter
					print('This was correct, no outer fringe, moving to next chapter')
					chapter_for_assessment = chapter_for_assessment[1::1]
					(question, current_node) = choose_question(request, temp_states, chapter_for_assessment, 1)
				

			else:
				incorrect  = incorrect + 1
				print('here number of question is', number_of_question)
				
				this_q = 0
				(question, current_node)= choose_question(request, temp_states, chapter_for_assessment, 0)
				if question is None or number_of_question > 5: 

					change_temp_state(request, chapter_for_assessment[0], current_node)
					print('new node created for chapter')


					# create a temp state
					if len(chapter_for_assessment) == 0:
						print("Quiz ends")
						student_state_ 					= UserState.objects.filter(user = user)
						if student_state_.exists():
							student_state 				= student_state_.first()
							student_state.active_part 	= 2
							student_state.save()
								
						return JsonResponse({'empty' : True})
					# assessment for this chapter is done: Move to next chapter
					print('This was incorrect, moving to next chapter')
					number_of_question = 0
					print('here number of question is', number_of_question)
					chapter_for_assessment = chapter_for_assessment[1::1]
					(question, current_node) = choose_question(request, temp_states, chapter_for_assessment, 1)



			if question is None:
				# if new chapter do not have any question
				if len(chapter_for_assessment) == 0:
						print("Quiz ends")
						student_state_ 					= UserState.objects.filter(user = user)
						if student_state_.exists():
							student_state 				= student_state_.first()
							student_state.active_part 	= 2
							student_state.save()
						return JsonResponse({'empty' : True})
					# assessment for this chapter is done: Move to next chapter
				chapter_for_assessment = chapter_for_assessment[1::1]
				(question, current_node) = choose_question(request, temp_states, chapter_for_assessment, 1)
				print(question, current_node)

				if question is None:
					print('Add more question please')
					student_state_ 						= UserState.objects.filter(user = user)
					if student_state_.exists():
							student_state 				= student_state_.first()
							student_state.active_part 	= 2
							student_state.save()
					return JsonResponse({'empty' : True})



			print('question  here is', question)
			pk 					= question.last().pk
			question_ 			= Question.objects.filter(pk = pk)
			current_question 	= question_.first()
			question  			= question_.values()


		


			json_context = {
				'question_image' : list(question),
				'empty'          : False
			}
			

			

			return JsonResponse(json_context)

							
def choose_question(request, temp_states, chapter_for_assessment, next):
	if len(chapter_for_assessment) == 0:
		print('No more chapter')
		return None, None
	chapter                      = chapter_for_assessment[0]
	print('Current active chapter is ', chapter)
	(domain_node, domain_count)  = utility_kst.domain_kstate(chapter)
	num_quiz_questions			 = number_optimum(domain_count)  

	temp_node 			 		 = temp_states.filter(chapter = chapter).first().node

	if next==1:   # if previous question submission is correct
		outer_fringe_state   = utility_kst.outer_fringe_states(temp_node)
		present_node         = utility_kst.outer_fringe(temp_node)
		print(outer_fringe_state)
		if len(outer_fringe_state) == 0:
			print('do something as no outer fringe is here for node', temp_node)

			return None, temp_node
		else:
			state_to_ask     = outer_fringe_state[0]
			change_temp_state(request, chapter, present_node[0])
			print('this has changed the temp node outer fringe to', present_node, outer_fringe_state)
			print('state to ask :', state_to_ask)
			questions        = Question.objects.filter(state = state_to_ask)
			print(questions)
			if questions.exists():
				return questions, present_node
			else:
				return None, present_node

	else:   # if previous question submission is incorrect
		outer_fringe_state   = utility_kst.inner_fringe_states(temp_node)
		present_node         = utility_kst.inner_fringe(temp_node)
		print(outer_fringe_state)
		if len(outer_fringe_state) == 0:
			print('do something as no inner fringe is here for node', temp_node)
			return None, temp_node
		else:
			print('current node is', temp_node)
			print('')
			print('inner fringe here is', outer_fringe_state)
			state_to_ask     = outer_fringe_state[0]
			questions        = Question.objects.filter(state = state_to_ask)
			change_temp_state(request, chapter, present_node[0])
			print('this has changed the temp node to', present_node, outer_fringe_state)
			if questions.exists():
				return questions, present_node
			else:
				return None, present_node



	

def assessment_report(request):
	user = request.user
	if user.is_authenticated:
		standard    = user.standard
		student_state_ = UserState.objects.filter(user = user)
		if student_state_.exists():
			student_state = student_state_.first()
			if student_state.active_part!=2:
				return redirect('assess:active')
		new_chapter    		= []
		know_chapter   		= []
		ready_to_learn 		= {}
		practice_chapter 	= []
		next_ready 			= {}
		next_ready_node 	= {}

		temp_nodes = TempActiveNode.objects.filter(user = user)
		chapters    = Chapter.objects.filter(standard = standard)   # SET STANDARD

		for chapter in temp_nodes:
			if chapter.node is None or chapter.dont_know_switch==1:
				new_chapter.append(chapter.chapter)
			else:
				node      = utility_kst.outer_fringe_id(chapter.node)
				new_nodes = utility_kst.outer_fringe_states(chapter.node)

				if len(node)!=0:
					next_ready_node[chapter.chapter] = node[0]
				if len(new_nodes) !=0:
					next_ready[chapter.chapter] = new_nodes[0]
				else:
					practice_chapter.append(chapter.chapter)


				
				know_chapter.append(chapter.chapter)


		for new in new_chapter:
			ch_nodes= Node.objects.filter(state_node__topic__chapter=new).distinct()
			for nd in ch_nodes:
				if nd.state_node.all().count()== 1:
					ready_to_learn[new.title] = nd

		for p in practice_chapter:

			if PracticeChapter.objects.filter( Q(user = user) & Q(chapter = p)).exists():
				continue
			else:

				PracticeChapter.objects.create(
					user = user,
					chapter = p
				)
		


		context ={

			'old' : next_ready,
			'new': ready_to_learn,
			'done' : practice_chapter,
			'node' : next_ready_node,

		}



	return render(request, 'userstates/report.html', context )



				



def start_chapter(request):
	user = request.user

	if user.is_authenticated:
		state_	 = request.POST.get('state', None)
		chapter_ = request.POST.get('chapter', None)
		node_    = request.POST.get('node', None)
		print(request.POST)

		if state_ and chapter_ and node_:
			node_    = int(node_)
			node 	 = Node.objects.get(id = node_)
			state    = State.objects.filter(tag = state_).first()

			current  = CurrentActiveNode.objects.filter(user = user)



			if current.exists():
				current.first().delete()

			current_state = CurrentActiveState.objects.filter(user = user)

			if current_state.exists():
				current_state.first().delete()

			CurrentActiveNode.objects.create(
				user    = user,
				node    = node,
			)
			CurrentActiveState.objects.create(
				user    = user,
				state   = state
			)

			student_state_ = UserState.objects.filter(user = user)
			if student_state_.exists():
				student_state = student_state_.first()
				student_state.active_part = 4
				student_state.save()
		else:
			print('Problem is that assessment, please try again')
			student_state_ = UserState.objects.filter(user = user)
			if student_state_.exists():
				student_state = student_state_.first()
				student_state.active_part = 0
				student_state.save()

		return redirect('assess:active')

		
   
	
def active_state(request):
	user = request.user
	if user.is_authenticated:
		student_state_ = UserState.objects.filter(user = user)
		if student_state_.exists():
			student_state = student_state_.first()
			if student_state.active_part == 0:
				return redirect('assess:initial-assess')
			elif student_state.active_part == 1:
				return redirect('assess:first')
			elif student_state.active_part == 2:
				return redirect('assess:report')
			elif student_state.active_part ==3:
				return redirect('assess:assign')
			elif student_state.active_part ==4:
				return redirect('content:show-content')
			else:
				return redirect('content:problem')


	










			


