from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import utility_kst
from .import forms




from .models import State, Node
from chapters.models import Chapter


def myview(request):
  return render(request, 'states/states.html', {'q': State.objects.all() })



def stateadmin(request):
    if request.user.is_authenticated:
        user_obj = request.user
        chapters=Chapter.objects.all() 
        topics=Topic.objects.all()
        states=State.objects.all()        

        if request.POST.get('add',False):
            return render(request, 'states/selectchapter.html', {'select_standard':1,'chapters':chapters, 'profile':user_obj})
      
      
        if request.POST.get('standard',False):
            standard=request.POST.get('standard',False)
            chapters=Chapter.objects.filter(standard=standard)
            return render(request, 'states/selectchapter.html', {'chapters':chapters, 'profile':user_obj})


        context = {'topics':topics, 
        'chapters':chapters, 
        'states':states, 
        'profile':user_obj}

        return render(request, 'states/stateadmin.html', context)
    else:
        return redirect('/auth/login/')



def stateedit(request, title, topic):
    if request.user.is_authenticated:
        user_obj = request.user
        
        if request.POST.get('delete',False):
                t=Topic.objects.get(title=topic)
                s=State.objects.get(title=title, topic=t)
                s.delete()
                chapters=Chapter.objects.all() 
                topics=Topic.objects.all()
                states=State.objects.all()

                context = {'state_deleted':1,
                'topics':topics, 
                'chapters':chapters, 
                'states':states, 
                'profile':user_obj}

                return render(request, 'states/stateadmin.html', context)

        elif request.POST.get('update',False):
            t=Topic.objects.get(title=topic)
            state=State.objects.get(title=title, topic=t)

            state_form = forms.state_form(request.POST, instance=state)
            if state_form.is_valid():
                updated_state = state_form.save(commit=False)
                updated_state.topic=t
                updated_state.save()
                return redirect('/states/admin/'+str(updated_state.title)+'/'+str(updated_state.topic)+'/')
            else:
                state_form = forms.state_form(instance=state)
                topics=Topic.objects.all()

                context = {'topics':topics, 
                'state':state,
                'state_update_error':1,
                'state_form':state_form, 
                'profile':user_obj}

                return render(request, 'states/stateedit.html', context)


            

        else:       
            topics=Topic.objects.all()
            t=Topic.objects.get(title=topic)
            state=State.objects.get(title=title, topic=t)

            state_form = forms.state_form(instance=state)
            
            return render(request, 'states/stateedit.html', {'topics':topics, 'state':state,'state_form':state_form, 'profile':user_obj})
    else:
        return redirect('/auth/login/')


def selectchapter(request,title):
     if request.user.is_authenticated:
        user_obj = request.user
        chapter=Chapter.objects.get(title=title)
        topics=Topic.objects.filter(chapter=chapter)
        print(topics)
        return render(request, 'states/selecttopic.html', {'topics':topics, 'profile':user_obj})
     else:
        return redirect('/auth/login/')


def selecttopic(request,title):
     if request.user.is_authenticated:
        user_obj = request.user
        topic=Topic.objects.get(title=title)

        if request.POST.get('add',False):
            state_form = forms.state_form(request.POST)
            if state_form.is_valid():
                new_state=state_form.save(commit=False)
                new_state.topic=topic
                new_state.save()
                
                chapters=Chapter.objects.all() 
                topics=Topic.objects.all()
                states=State.objects.all()

                context = {'state_added':1,
                'topics':topics, 
                'chapters':chapters, 
                'states':states, 
                'profile':user_obj}

                return render(request, 'states/stateadmin.html', context)  

            else:
                state_form = forms.state_form()

                context = {'state_add_error':1,
                'state_form':state_form,
                'topics':topic, 
                'profile':user_obj}

                return render(request, 'states/addstate.html', context)



        
        state_form = forms.state_form()
        return render(request, 'states/addstate.html', {'state_form':state_form,'topics':topic, 'profile':user_obj})
     else:
        return redirect('/auth/login/')


# def nodeadmin(request):
#         if request.user.is_authenticated:
#             user_obj = request.user
#             nodes=Node.objects.all()
#             chapters= Chapter.objects.all()


#             if request.POST.get('standard',False):
#                 standard=request.POST.get('standard',False)
#                 chapters=Chapter.objects.filter(standard=standard)

#                 context= {'chapter_select':1,
#                 'chapters':chapters,
#                 'nodes':nodes, 
#                 'profile':user_obj}

#                 return render(request, 'states/nodeadmin.html', context)



#             return render(request, 'states/nodeadmin.html', {'chapters':chapters,'nodes':nodes, 'profile':user_obj})
#         else:
#             return redirect('/auth/login/')


# def nodeedit(request, nodeid):
#     if request.user.is_authenticated:
#         user_obj = request.user
#         node=Node.objects.get(id=nodeid)

#         if request.POST.get('delete',False):
#             node.delete()
#             nodes=Node.objects.all()
#             chapters= Chapter.objects.all()

#             context = {'node_deleted':1,
#             'chapters':chapters,
#             'nodes':nodes, 
#             'profile':user_obj}

#             return render(request, 'states/nodeadmin.html', context)

#         if request.POST.get('update',False):
#             node_form = forms.node_form(request.POST,instance=node)
#             if node_form.is_valid():
#                 node_form.save()                
#                 return redirect('/states/admin/node/'+str(node.id)+'/')

#             else:
#                 node_form = forms.node_form(instance=node)

#                 context = {'node_update_error':1,
#                 'node_form':node_form,
#                 'node':node, 
#                 'profile':user_obj}

#                 return render(request, 'states/nodeedit.html', context)


#         node_form = forms.node_form(instance=node)
#         return render(request, 'states/nodeedit.html', {'node_form':node_form,'node':node, 'profile':user_obj})
#     else:
#         return redirect('/auth/login/')



# def addnode(request,chapid):
#     if request.user.is_authenticated:
#         if request.POST.get('addnode',False):
#             user_obj = request.user

#             node_form = forms.node_form(request.POST)
#             if node_form.is_valid():
#                 description=node_form.cleaned_data['description']
#                 credit=node_form.cleaned_data['credit']
#                 selected_states=list()
#                 states=State.objects.all()
            
#                 for i in states:
#                     if request.POST.get(str(i.id)):
#                         selected_states.append(i)

#                 nodes=Node.objects.all()
#                 for i in nodes:
#                     if list(i.state_node.all()) == selected_states:
#                         c=Chapter.objects.get(id=chapid)
#                         states= State.objects.filter(topic__chapter=c)
#                         user_obj = request.user

#                         node_form = forms.node_form()

#                         context = {'node_exists_error':1,
#                         'node_form':node_form,
#                         'chapter':c,
#                         'states':states, 
#                         'profile':user_obj}

#                         return render(request, 'states/addnode.html', context)


#                 newnode= Node()
#                 newnode.description=description
#                 newnode.credit=credit
#                 newnode.save()

#                 for i in selected_states:
#                     newnode.state_node.add(i)
#                     print(newnode.state_node.all())

#                 nodes=Node.objects.all()
#                 chapters= Chapter.objects.all()
                
#                 context = {'node_added':1,
#                 'chapters':chapters,
#                 'nodes':nodes, 
#                 'profile':user_obj}

#                 return render(request, 'states/nodeadmin.html', context)     

#         states=list() 
#         c=Chapter.objects.get(id=chapid)
#         states= State.objects.filter(topic__chapter=c)
#         user_obj = request.user

#         node_form = forms.node_form()
#         return render(request, 'states/addnode.html', {'node_form':node_form,'chapter':c,'states':states, 'profile':user_obj})
#     else:
#         return redirect('/auth/login/')

