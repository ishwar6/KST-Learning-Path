from django.shortcuts import render, redirect
from django.db.models import Q, Count
from chapters.models import Chapter, Topic
from userstates.models import PracticeChapter, TempActiveNode
from states.models import State, Node
import utility_kst as u
from django.utils import timezone
from chapters.models import Topic
from django.contrib import messages
from django.db import transaction
from questions.models import Question, QuestionResponse
from django.http import JsonResponse
from content.models import (    Content,
                                Illustration, 
                                CompletedChapter,
                                PreviousState, 
                                CurrentActiveState,
                                CompletedState,
                                CurrentActiveNode,
                                PreviousActiveNode,

                         )












def change_chapter(request):
    '''It returns chapter report of a student'''
    user = request.user
    if user.is_authenticated:
        student_state_          = CurrentActiveState.objects.filter(user= user)
        if student_state_.exists():
            standard            = user.standard
            student_state       = student_state_.first()
# to get current chapter and to save it in completedchapter
            state               = student_state.state.id
            current_topic       = State.objects.filter(pk = state).first().topic
            current_chapter_pk  = Topic.objects.filter(title = current_topic).first().chapter.id
            current_chapter     = Chapter.objects.filter(pk = current_chapter_pk).first()
            temp_active_node    = TempActiveNode.objects.filter(user = user)
                # to access practice chapter from userstates nodes

            practice_chapter             = PracticeChapter.objects.filter(user = user)
            chapters                     = Chapter.objects.filter(standard = standard) 
            comp_chapters                = CompletedChapter.objects.filter(user = user)
            list_of_chapters_incomp      = []
            list_of_chapters_to_practice = []
            list_of_chapters_done        = []
            list_of_other_chapter        = []
            list_of_current              = []
            list_of_current.append(current_chapter)
           # dict_incomplete_chapter = {}

            for p in practice_chapter:
                list_of_chapters_to_practice.append(p.chapter)
            for c in comp_chapters:
                if c.node is None and c.done==1:
                    list_of_chapters_done.append(c.chapter)
                else:
                    list_of_chapters_incomp.append(c.chapter)
                  #  dict_incomplete_chapter[c.chapter] = c.node
            for t in temp_active_node:
                list_of_other_chapter.append(t.chapter)
            a = list(set(list_of_other_chapter) - set(list_of_chapters_done) - set(list_of_chapters_incomp) - set(list_of_chapters_to_practice) -set(list_of_current) )
            context  = {

                'completed_chapters' : list_of_chapters_done,
                'incomplete_chapters': list_of_chapters_incomp,
                'practice_chapters'  : list_of_chapters_to_practice,
                'left_chapters'      : a,
                'current_chapter'    : current_chapter, 
            }
            return render(request, 'content/chapter.html', context )


# import Checksum
# import requests
# import base64
# import json


# def change_chapter(request):
#         MERCHANT_KEY = '1ZcaXo_Ih2zGM1@@';
#         data_dict = {
#         'MID':'HOMETA49432079784489',
#         'ORDER_ID':'dddgfgfjhjgjwerr324235523dsfeeed',
#         # 'TXN_AMOUNT':'1.00',
#         # 'CUST_ID':'iisudrj26@gmail.com',
#         # 'INDUSTRY_TYPE_ID':'Retail',
#         # 'WEBSITE':'WEBSTAGING',
#         # 'CHANNEL_ID':'WEB',
#         #'CALLBACK_URL':'http://localhost/pythonKit/response.cgi',
#         }


#         param_dict = data_dict 
#         param_dict['CHECKSUMHASH'] =Checksum.generate_checksum(data_dict, MERCHANT_KEY)

#         context = {
#             'data' : param_dict
#         }

     

#         return render(request, 'content/chapter.html', context )






            
def switch_chapter(request, id = None, s=0):
    print('In switch chapter function')
    id = int(id)
    s = int(s)
    print(id, s)
    # if s=0 it is new chapter, it is 1 if it is incomplete, 2 if it is in practice
    # for new (s=0) jump to outer fringe of user temp node else be in very same node ( if s= 1 or 2)

    user = request.user 
    chapter = Chapter.objects.filter(id=id).first()
    if user.is_authenticated and id is not None:
        active_node             = CurrentActiveNode.objects.filter(user = user)
        if active_node.exists():
            active_node         = active_node.first()
            active_node         = active_node.node
        else:
            active_node = None
        student_state_          = CurrentActiveState.objects.filter(user= user)
        if student_state_.exists():
            standard            = user.standard
            student_state       = student_state_.first()
        else:
            student_state = None


        if s==0:
            
            # jump to outer fringe of temp node
            temp_node     = TempActiveNode.objects.filter( Q(user = user) & Q(chapter = chapter) ).first()
            if temp_node.dont_know_switch ==1:
                # if he don't know the chapter assign the very first state else go to outer fringe
                
                fav_state, fav_node = u.first_state_and_node(chapter)
                chapter_save(request, id, 0, fav_node)
                change_previous_state(request, student_state)
                change_active_state(request, fav_state, fav_node , student_state, active_node)
                return redirect('content:active')

            else:
                # if student knows something then goto tempstate directly as it is brand new chapter

                fav_node  = temp_node.node
                fav_state = fav_node.state_node.all().first()
                chapter_save(request, id, 0, fav_node)
                change_previous_state(request, student_state)
                change_active_state(request, fav_state, fav_node , student_state, active_node)

                print(fav_state)
                print('this is new')
                return redirect('content:active')

        if s==1:
            # now be in very same node
            incomp_chapter = CompletedChapter.objects.filter( Q(user = user) & Q(chapter = chapter) ).first()
            fav_node       = incomp_chapter.node
            fav_state = fav_node.state_node.all().first()
            chapter_save(request, id, 0, fav_node)
            change_previous_state(request, student_state)
            change_active_state(request, fav_state, fav_node , student_state, active_node)
            return redirect('content:active')

     



        

def chapter_save(request, id, s = 0,  fav_node=None):
    '''To save chapter in incomplete state. If s is 1 then done is true. '''
    user    = request.user
    chapter = Chapter.objects.filter(id = id).first()
    old_save = CompletedChapter.objects.filter( Q(user = user) & Q(chapter = chapter) )
    if old_save.exists():
        old_save.first().delete()
    
    if s==0:
        CompletedChapter.objects.create(
            user = user,
            chapter = chapter,
            node = fav_node

        )
    else:
        CompletedChapter.objects.create(
            user = user,
            chapter = chapter,
     
            done = 1

        )
    print('Incomplete chapter added', chapter)
    return True














def change_previous_state(request, student_state, score = 0):
    '''It takes student_state instance and delete previous state if any,
         for this state and creates a new previous state with
            updated score and illustration points     '''


    user = request.user
    if_old = PreviousState.objects.filter(Q(user = user) & Q(state = student_state.state))

    if if_old.exists():
        if_old = if_old.first()
        score_of_i_old = if_old.score_of_i
        score_of_q_old = if_old.score_of_q
        if_old.delete()
    else:
        score_of_i_old = 0
        score_of_q_old = 0

    PreviousState.objects.create(
        user            = user,
        state           = student_state.state,
        score           = score,
        score_of_i      = student_state.score_of_i + score_of_i_old,
        score_of_q      = student_state.score_of_q + score_of_q_old, 

    )
    print('Previous state updated')
    return True

        
def change_active_state(request, fav_state, fav_node, student_state = None ,   active_node = None):
    '''It takes current active node, to make it previous active node. It takes
    fav node  and fav_state to create a new active node and active state. It deletes previous student_state also. '''

    user = request.user
    with transaction.atomic():
        if active_node is not None:

            PreviousActiveNode.objects.create(  
                user = user,
                node = active_node
            )
        if student_state is not None:
            student_state.delete()

        current_active_node = CurrentActiveNode.objects.filter(user = user)


        if current_active_node.exists():
            current_active_node.first().delete()


        CurrentActiveNode.objects.create(
            user = user,
            node = fav_node
        )
        print('current state and nodes activated and updated')
       
        CurrentActiveState.objects.create(
            user = user,
            state = fav_state,
                )
        
    return True


          









def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'content/dashboard.html', {})



def Diff(li1, li2): 
    return (list(set(li1) - set(li2)))


def problem(request):
    return render(request, 'content/error.html', {})


def active_part_redirect(request):
    user = request.user
    if user.is_authenticated:
        student_state_  = CurrentActiveState.objects.filter(user= user)
        if student_state_.exists():
            student_state = student_state_.first()
            if student_state.active_part == 1:
                return redirect('content:show-content')
            elif student_state.active_part == 2:
                return redirect('content:illustrations')
            elif student_state.active_part == 3:
                return redirect('content:questions')
            elif student_state.active_part ==4:
                return redirect('content:report')
            else:
                return redirect('content:report')
            
            





def assignstate(request, id, s):
    user = request.user
    if user.is_authenticated:
        student_state_  = CurrentActiveState.objects.filter(user= user)

        
        if student_state_.exists():
            s = int(s)
            id = int(id)
            student_state = student_state_.first()
            if student_state.active_part != 5:
                return redirect('content:active')

            
            active_node = CurrentActiveNode.objects.filter(user = user)
            if active_node.exists():
                active_node = active_node.first()
                active_node = active_node.node

            active_old = active_node
            fav_node = None

            if s == 0:
                back = u.inner_fringe(active_node)
                print(back)
                new_state = State.objects.filter(id = id).first()
                if len(back)==0:
                    fav_node = active_old
                else:
                    for node in back:
                        if new_state in node.state_node.all():
                            fav_node = node
                            continue
                if fav_node is None:
                    fav_node = active_node



                with transaction.atomic():
                    PreviousActiveNode.objects.create(  
                        user = user,
                        node = active_node
                    )
                    
                    CurrentActiveNode.objects.filter(user = user).delete()
                    CurrentActiveNode.objects.create(
                        user = user,
                        node = fav_node
                    )
                    student_state_.delete()
                    CurrentActiveState.objects.create(
                        user = user,
                        state = new_state,
                            )

            if s == 1:
                forward = u.outer_fringe(active_node)
                chapter_id   = student_state.state.topic.chapter.id
                
               

                if len(forward) == 0:
                    chapter_save(request, chapter_id, 1, None)

                    print('outer fringe empty for this chapter')
                    return redirect('content:details-chapter')

                new_state = State.objects.filter(id = id).first()

                for node in forward:
                    if new_state in node.state_node.all():
                        fav_node = node
                        break
                with transaction.atomic():

                    PreviousActiveNode.objects.create(
                        user = user,
                        node = active_node
                    )
                    
                    CurrentActiveNode.objects.filter(user = user).delete()
                    CurrentActiveNode.objects.create(
                        user = user,
                        node = fav_node
                    )
                    student_state_.delete()
                    CurrentActiveState.objects.create(
                        user = user,
                        state = new_state,
                        
                    )
    return redirect('content:show-content')


def showcontent(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        student_state  = CurrentActiveState.objects.filter(user= user)
        if student_state.exists():
            student_state = student_state.first()
            if student_state.active_part !=1:
                return redirect('content:active')
            content = Content.objects.filter(state = student_state.state)
            if content.exists():
                content = content.first()

            context = {
                'state'  : student_state.state,
                'content': content
            }


        if request.method == 'POST':
            student_state.active_part = 2
            student_state.save()
            return redirect('content:illustrations')



    return render(request, 'content/page.html' , context)



      

    



def show_illustrations(request, content = None):
    user = request.user
    message = ''
    if user.is_authenticated:
        student_state  = CurrentActiveState.objects.filter(user = user)
       
        student_state = student_state.first()
        if student_state.active_part  != 2:
            return redirect('content:active')
        
        
        state = student_state.state
        content = Content.objects.filter(state = state)
        print(content)
        if content.exists():
            content = content.first()
        else:
            print('Please add content first for state', state)

        student_illus_point   = illus_pt_this_state = student_state.score_of_i
        score_of_illus_needed  = state.score_of_i()
        print(student_illus_point)


        previous_state = PreviousState.objects.filter(Q(user = user) & Q(state = state))
        print('previous state is', previous_state)
        if previous_state.exists():
            previous_state = previous_state.first()
            student_illus_point = student_illus_point + previous_state.score_of_i 
        print(student_illus_point)

        percentage_remaining   = ( illus_pt_this_state / score_of_illus_needed ) * 100
        illustration           = Illustration.objects.filter(content = content)

        illustrations_to_render = []
        while(illus_pt_this_state < score_of_illus_needed):
            student_illus_point    = student_illus_point + 1
            illus_pt_this_state     = illus_pt_this_state + 1
            illus_now        = illustration.filter(counts = student_illus_point)
            if illus_now.exists():
                illustrations_to_render.append(illus_now.first())
                student_illus_point    = student_illus_point - 1
                
            else:

                message = ' Our Fault: Sorry dear, no illustrations at this time. Please Move forward to Questions '
                break

        if illus_pt_this_state >= score_of_illus_needed:
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
            #now active part is 3 for this student 
            student_state.active_part = 3
            student_state.save()
            return redirect('content:questions')


    return render(request, 'content/illus.html', context)

       
















def show_questions(request):
    user = request.user
    message = ''
    global questions, percentage_remaining, student_ques_point, score_of_ques_needed, questions_to_render, q, student_state, current_question, correct, incorrect
    global number_of_questions
    if user.is_authenticated:
        if request.method == 'GET':
            correct = incorrect = 0
            student_state  = CurrentActiveState.objects.filter(Q(user = user))
            if student_state.exists():
                student_state = student_state.first()
                if student_state.active_part  != 3:
                    return redirect('content:active')
                state         = student_state.state

                student_ques_point  = q = student_ques_point_overall  = student_state.score_of_q
                score_of_ques_needed   = state.score_of_q()

                percentage_remaining   = ( student_ques_point / score_of_ques_needed ) * 100
                previous_state = PreviousState.objects.filter(Q(user = user) & Q(state = state))
                if previous_state.exists():
                    previous_state = previous_state.first()
                    student_ques_point_overall = student_ques_point_overall + previous_state.score_of_q


                questions              = Question.objects.filter(state = state)
                count                  = student_ques_point_overall + 1

                questions_to_render = []

                #### ADD FURTHER COUNTS HERE   # # # ## # ## # ## # # # # # # #  ### # #  # # # #  # #  #######

                while(student_ques_point < score_of_ques_needed):
                    print(student_ques_point, score_of_ques_needed)
                    ques_now              = questions.filter(counts = count)
                    if ques_now.exists():
                        ques_now              = ques_now.first()
                        student_ques_point    = student_ques_point + int(ques_now.difficulty) 
                        count    = count + 1
                        questions_to_render.append(ques_now)
                        print(questions_to_render)
                    
                    else:
                        break

                        # render very first question by GET request
                number_of_questions     = len(questions_to_render)
                if number_of_questions == 0:
                    print('No question found for this state in datebase')
                    previous_state = PreviousState.objects.filter(Q(user = user) & Q(state = state))
                    if previous_state.exists():
                        previous_state              = previous_state.first()
                        previous_state.score_of_q   = 0 
                        previous_state.save()
                        return redirect('content:active')



                   
                current_question        = questions_to_render[0]
                questions_to_render     = questions_to_render[ 1::1]


                context = {
                    'currentquestion' : current_question,
                    'message'        : message,
                    'per_remaining'  : percentage_remaining,

                }

                return render(request, 'content/ques.html', context)



        if request.method == 'POST':
                student_state  = CurrentActiveState.objects.filter(user = user).first()
                if student_state.active_part  != 3:
                    return redirect('content:active')

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
                correct_answer_submission=0
                if op1==current_question.op1 and op2==current_question.op2 and op3==current_question.op3 and op4==current_question.op4 and integer_type_submission==current_question.integeral_answer:
                    correct_answer_submission = 1


                if correct_answer_submission==1:
                    correct = correct + 1
                    this_q = 1
                    message = ' Correct Answer, Nice!! '
                else:
                    incorrect  = incorrect + 1
                    this_q = 0
                    message = 'Incorrect Answer, Be careful next time. You can review all attempted questions by you in ACTIVITY tab'
                

                if len(questions_to_render) == 0:
                    previous_response = QuestionResponse.objects.filter(Q(user = user) & Q(question = current_question))
                    if previous_response.exists():
                        previous_response.first().delete()

                    QuestionResponse.objects.create(
                                user     = user,
                                question = current_question,
                                op1      = op1,
                                op2      = op2,
                                op3      = op3, 
                                op4      = op4,
                                integer_type_submission = integer_type_submission,
                                correct = this_q
                             )
                    q  =  q + 1 
                    student_state.score_of_q = q

                    # Now active part is 4 for this student for this state
                    student_state.active_part = 4
                    student_state.save()
                    messages.error(request, 'Congrulations!, you have successfully completed this state.')
                    return JsonResponse({'empty' : True})

              
                previous_response = QuestionResponse.objects.filter(Q(user = user) & Q(question = current_question))
                if previous_response.exists():
                    previous_response.first().delete()

                QuestionResponse.objects.create(
                                user     = user,
                                question = current_question,
                                op1      = op1,
                                op2      = op2,
                                op3      = op3, 
                                op4      = op4,
                                integer_type_submission = integer_type_submission,
                                correct = this_q
                                                  )

                current_question       = questions_to_render[0]
                ques_ = Question.objects.filter(id = current_question.pk).values()
                questions_to_render  = questions_to_render[ 1::1]
                q  =  q + 1 
                print('q is inthis', q)
                student_state.score_of_q = q
                student_state.save()
                percentage_remaining   = ( q / number_of_questions ) * 100

                json_context = {
                    'question' : 'this is the question',
                    'percentage': percentage_remaining,
                    'message': message,
                    'empty' : False,
                    
                   
                    'question_image' : list(ques_)

                }
                print(json_context)
                return JsonResponse(json_context)
                        





        

def report(request):
    user = request.user
    global score, student_state
    if user.is_authenticated:
        if request.method == 'GET':
            student_state = CurrentActiveState.objects.filter(Q(user = user)).first()
            if student_state.active_part  != 4:
                if student_state.active_part  == 5:
                    student_state.active_part = 4
                    student_state.save()
                return redirect('content:active')
            count         = student_state.score_of_q
            question_solved = QuestionResponse.objects.filter(Q(question__counts__lte = count) & Q( question__state = student_state.state ) )
            i  = j = wi = wc = 0 
        

            for a in question_solved:
                if a.correct is True:
                    i = i + 1
                    wc = wc + int(a.question.difficulty)
                else:
                    j = j + 1
                    wi = wi + int(a.question.difficulty)

            score =  (wc / (wc + wi)) * 100
            duration     = timezone.now() - student_state.timestamp
            days, seconds = duration.days, duration.seconds
            time_taken = days * 24 + seconds // 3600
            student_state.score = score
            student_state.save()

            if score >= 50:
                if_old = CompletedState.objects.filter(Q(user = user) & Q(state = student_state.state))
                if if_old.exists():
                    if_old = if_old.first()
                    if_old.delete()


                a = CompletedState.objects.create(
                    user        = user,
                    state       = student_state.state,
                    success     = 1,
                    correct     = i,
                    incorrect   = j,
                    time_taken  = time_taken,
                    score       = score,
                )
            else:
                if_old = PreviousState.objects.filter(Q(user = user) & Q(state = student_state.state))

                if if_old.exists():
                    if_old = if_old.first()
                    score_of_i_old = if_old.score_of_i
                    score_of_q_old = if_old.score_of_q
                    if_old.delete()
                else:
                    score_of_i_old = 0
                    score_of_q_old = 0

                PreviousState.objects.create(
                    user            = user,
                    state           = student_state.state,
                    score           = score,
                    score_of_i      = student_state.score_of_i + score_of_i_old,
                    score_of_q      = student_state.score_of_q + score_of_q_old, 

                )
                a = None

            
        # back_ = u.outer_fringe(chapter, active_node)
    

            context = {
                'question_solved' : question_solved,
                'state'           : student_state.state,
                'time'            : student_state.timestamp,
                'result'          : a,
                'score'           : score,

            }
            print(context)

        if request.method == 'POST':
            student_state = CurrentActiveState.objects.filter(Q(user = user)).first()
            if student_state.active_part!=4:
                return redirect('content:active')
            student_state = CurrentActiveState.objects.filter(user = user).first()
            student_state.active_part = 5
            student_state.save()
            active_node  = CurrentActiveNode.objects.filter(user = user).first().node
            score        = student_state.score
            
            state_list = []
            if score >= 50:
                upgrade = True
                success = 1
                states =  u.outer_fringe_states(active_node)
                print(states)

                if states is None:
                    messages.error(request, 'No outer fringe found. Make a new suitable node')
                    print("No outer fringe found. Make a new suitable node")
                    return redirect("content:problem")
                
                
            else:
                upgrade = False
                success = 0

                states =  u.inner_fringe_states(active_node)
                if len(states)==0:
                    list_student_know = []
                    for a in active_node.state_node.all():
                        list_student_know.append(a)
                    states = list_student_know
                    


                

            context = {
            'states' : states,
            'state'  : student_state.state,
            'upgrade': upgrade,
            'success' : success,
                }
            print(context)

    return render(request, 'content/report.html', context)






    # create current active node and current active state
    

    
       
def previous_content(request):
    user = request.user
    if user.is_authenticated:
        active_node = CurrentActiveNode.objects.filter(user = user)
        for node in active_node:
            a = node.node

        for state in a.state_node.all():
            print(state.title, state.topic)

    return True

       
       

		





    
        
    

   




