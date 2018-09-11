from django.shortcuts import render, redirect
from django.db.models import Q, Count
from chapters.models import Chapter, Topic
from userstates.models import UserCurrentNode, TempActiveNode
from states.models import State, Node
import utility_kst as u
from django.contrib import messages

from content.models import (    Content,
                                Illustration, 
                                IllustrationGiven,
                                CurrentActiveChapter, 
                                CurrentActiveState 
                         )




def Diff(li1, li2): 
    return (list(set(li1) - set(li2)))


# this function shows all possible states to cover for a particular user. 
def show_list_of_states(request, chapter = None):
    user = request.user
    chapter = Chapter.objects.filter(title__contains = 'number').first()
    if user.is_authenticated() and chapter is not None:
       

        # list is storing the individual state id's a student knows in a particular chapter
        user_active_node       = UserCurrentNode.objects.filter(Q(user = user) & Q(chapter = chapter)).first().node
        ready_to_learn         = u.outer_fringe_id(chapter, user_active_node)
        list_student_know = []
        topics_to_learn = []
        list_ready_toknow = []
        for a in user_active_node.state_node.all():
            list_student_know.append(a.id)

        for index in ready_to_learn:

            a = Node.objects.filter(id=index).first()

            for n in a.state_node.all():
                list_ready_toknow.append(n.id)
            
            topics_to_learn  = list (set(topics_to_learn + Diff(list_ready_toknow, list_student_know)))

        if len(topics_to_learn) != 0:
            return topics_to_learn
        else:
             return None
    return None


def showcontent(request, state = None):
    user = request.user
    state = State.objects.filter(pk = 2).first()
    if user.is_authenticated() and state is not None:
        student_state  = CurrentActiveState.objects.filter(Q(user = user) and Q(state = state))
        if student_state.exists():
            student_state = student_state.first()
        else:
            student_state = CurrentActiveState.objects.create(
                user = user, state = state, theory= 0
            )
        

        score_of_illus_needed  =   state.score_of_i()
        score_of_ques_needed   =   state.score_of_q()

        content  =  Content.objects.filter(state = state)
        if content.exists():
            content  = content.first()

        context = {
            'content' : content,
            'state'   : state,

        }

    return render(request, 'content/page.html', context)



def show_illustrations(request, content = None):
    user = request.user
    content = Content.objects.filter(pk = 2).first()
    state   = content.state
    message = ''
    if user.is_authenticated() and content is not None:
        student_state  = CurrentActiveState.objects.filter(Q(user = user) and Q(state = state))
        if student_state.exists():
            student_state = student_state.first()
        else:
            student_state = CurrentActiveState.objects.create(
                user = user, state = state, theory= 0
            )

        student_illus_point    = student_state.score_of_i
        score_of_illus_needed  = state.score_of_i()

        percentage_remaining   = ( student_illus_point / score_of_illus_needed ) * 100
        illustration           = Illustration.objects.filter(content = content)

        illustrations_to_render = []
        while(student_illus_point < score_of_illus_needed):
            student_illus_point    = student_illus_point + 1
            illus_now        = illustration.filter(counts = student_illus_point)
            if illus_now.exists():
                illustrations_to_render.append(illus_now)
                
            else:
                student_illus_point    = student_illus_point - 1

                message = ' Our Fault: Sorry dear, no illustrations at this time. Please Move forward to Questions '
                break

        if student_illus_point >= score_of_illus_needed:
            messages.error(request, 'hello, you have already completed your illustrations for this state')

        
        context = {
            'illus'          : illustrations_to_render,
            'content'        : content,
            'message'        : message,
            'per_remaining'  : percentage_remaining,

        }


   #  If student submits because he has completed the illustrations 
        if request.method == 'POST':
            student_state.score_of_i = student_illus_point
            student_state.save()
            return redirect('content:questions')


    return render(request, 'content/illus.html', context)

       













def show_questions(request):

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
			print("Correct!!")

        return render(request, 'content/ques.html', {})
