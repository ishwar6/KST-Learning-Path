from django.shortcuts import render, redirect
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import utility_kst
from .import forms

kst = importr('kst')


from .models import State, Node, Edge, Topic
from chapters.models import Chapter


def myview(request):
  return render(request, 'states/states.html', {'q': State.objects.all() })


def nodes(request):
    edges= Edge.objects.all()
    n = Node.objects.all()
    
    kstr= utility_kst.nodes2kstructure(n) #modification to test the new utility_kst package

    ksp = kst.kspace(kstr)
    lp = kst.lpath(kstr)
    list = kst.lpath_is_gradation(lp)



    context = {     'q': n,
                    'e': edges,
                    'lp': lp,
                    'ksp': ksp
              }

    return render(request, 'states/states.html', context)



def stateadmin(request):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
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
        user_obj = User.objects.get(username=request.user)
        
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
                return render(request, 'states/stateedit.html', {'topics':topics, 'state':state,'state_update_error':1,'state_form':state_form, 'profile':user_obj})


            

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
        user_obj = User.objects.get(username=request.user)
        chapter=Chapter.objects.get(title=title)
        topics=Topic.objects.filter(chapter=chapter)
        print(topics)
        return render(request, 'states/selecttopic.html', {'topics':topics, 'profile':user_obj})
     else:
        return redirect('/auth/login/')


def selecttopic(request,title):
     if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
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
                return render(request, 'states/addstate.html', {'state_add_error':1,'state_form':state_form,'topics':topic, 'profile':user_obj})



        
        state_form = forms.state_form()
        return render(request, 'states/addstate.html', {'state_form':state_form,'topics':topic, 'profile':user_obj})
     else:
        return redirect('/auth/login/')


def nodeadmin(request):
        if request.user.is_authenticated:
            user_obj = User.objects.get(username=request.user)
            nodes=Node.objects.all()
            chapters= Chapter.objects.all()


            if request.POST.get('standard',False):
                standard=request.POST.get('standard',False)
                chapters=Chapter.objects.filter(standard=standard)
                return render(request, 'states/nodeadmin.html', {'chapter_select':1,'chapters':chapters,'nodes':nodes, 'profile':user_obj})



            return render(request, 'states/nodeadmin.html', {'chapters':chapters,'nodes':nodes, 'profile':user_obj})
        else:
            return redirect('/auth/login/')


def nodeedit(request, nodeid):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
        node=Node.objects.get(id=nodeid)

        if request.POST.get('delete',False):
            node.delete()
            nodes=Node.objects.all()
            chapters= Chapter.objects.all()

            context = {'node_deleted':1,
            'chapters':chapters,
            'nodes':nodes, 
            'profile':user_obj}

            return render(request, 'states/nodeadmin.html', context)

        if request.POST.get('update',False):
            node_form = forms.node_form(request.POST,instance=node)
            if node_form.is_valid():
                node_form.save()                
                return redirect('/states/admin/node/'+str(node.id)+'/')

            else:
                node_form = forms.node_form(instance=node)
                return render(request, 'states/nodeedit.html', {'node_update_error':1,'node_form':node_form,'node':node, 'profile':user_obj})


        node_form = forms.node_form(instance=node)
        return render(request, 'states/nodeedit.html', {'node_form':node_form,'node':node, 'profile':user_obj})
    else:
        return redirect('/auth/login/')



def addnode(request,chapid):
    if request.user.is_authenticated:
        if request.POST.get('addnode',False):
            user_obj = User.objects.get(username=request.user)

            node_form = forms.node_form(request.POST)
            if node_form.is_valid():
                description=node_form.cleaned_data['description']
                credit=node_form.cleaned_data['credit']
                selected_states=list()
                states=State.objects.all()
            
                for i in states:
                    if request.POST.get(str(i.id)):
                        selected_states.append(i)

                nodes=Node.objects.all()
                for i in nodes:
                    if list(i.state_node.all()) == selected_states:
                        c=Chapter.objects.get(id=chapid)
                        states= State.objects.filter(topic__chapter=c)
                        user_obj = User.objects.get(username=request.user)

                        node_form = forms.node_form()
                        return render(request, 'states/addnode.html', {'node_exists_error':1,'node_form':node_form,'chapter':c,'states':states, 'profile':user_obj})


                newnode= Node()
                newnode.description=description
                newnode.credit=credit
                newnode.save()

                for i in selected_states:
                    newnode.state_node.add(i)
                    print(newnode.state_node.all())

                nodes=Node.objects.all()
                chapters= Chapter.objects.all()
                
                context = {'node_added':1,
                'chapters':chapters,
                'nodes':nodes, 
                'profile':user_obj}

                return render(request, 'states/nodeadmin.html', context)     

        states=list() 
        c=Chapter.objects.get(id=chapid)
        states= State.objects.filter(topic__chapter=c)
        user_obj = User.objects.get(username=request.user)

        node_form = forms.node_form()
        return render(request, 'states/addnode.html', {'node_form':node_form,'chapter':c,'states':states, 'profile':user_obj})
    else:
        return redirect('/auth/login/')


 
def edgeadmin(request):
    if request.user.is_authenticated:
            user_obj = User.objects.get(username=request.user)
            edges=Edge.objects.all()
            chapters= Chapter.objects.all()

            if request.POST.get('standard',False):
                standard=request.POST.get('standard',False)
                chapters=Chapter.objects.filter(standard=standard)
                return render(request, 'states/edgeadmin.html', {'chapter_select':1,'chapters':chapters,'edges':edges, 'profile':user_obj})


            return render(request, 'states/edgeadmin.html', {'chapters':chapters,'edges':edges, 'profile':user_obj})
    else:
        return redirect('/auth/login/')


def edgeedit(request, edgeid):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
        edge=Edge.objects.get(id=edgeid)

        if request.POST.get('delete',False):
            edge.delete()
            edges=Edge.objects.all()
            chapters= Chapter.objects.all()

            context = {'edge_deleted':1,
            'chapters':chapters,
            'edges':edges, 
            'profile':user_obj}

            return render(request, 'states/edgeadmin.html', context)

        if request.POST.get('update',False):
            edge_form = forms.edge_form(request.POST,instance=edge)
            if edge_form.is_valid():
                edge_form.save()                          
                return redirect('/states/admin/edge/'+str(edge.id)+'/')

        edge_form = forms.edge_form(instance=edge)
        return render(request, 'states/edgeedit.html', {'edge_form':edge_form,'edge':edge, 'profile':user_obj})
    else:
        return redirect('/auth/login/')



def addedge(request,chapid):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
        if request.POST.get('addedge',False):
            edge_form = forms.edge_form(request.POST)
            if edge_form.is_valid():
                weight=edge_form.cleaned_data['weight']
                time=edge_form.cleaned_data['time']

                addnodes=list()
                nodes=Node.objects.all()
                for i in nodes:
                    if request.POST.get(str(i.id)):
                        addnodes.append(i)

                if len(addnodes)!=2:
                    c=Chapter.objects.get(id=chapid)
                    chapter_nodes=list()
                    chapter_nodes = nodes= Node.objects.filter(state_node__topic__chapter=c).distinct()
                    edge_form = forms.edge_form()
                    return render(request, 'states/addedge.html', {'two_nodes_needed_error':1,'edge_form':edge_form,'chapter':c,'nodes':chapter_nodes, 'profile':user_obj})



                n1=addnodes[0]
                n2=addnodes[1]

                all_edges=Edge.objects.all()
                for i in all_edges:
                    if (i.first==n1 and i.second==n2) or (i.first==n2 and i.second==n1):
                        c=Chapter.objects.get(id=chapid)
                        chapter_nodes=list()
                        chapter_nodes = nodes= Node.objects.filter(state_node__topic__chapter=c).distinct()
                        edge_form = forms.edge_form()
                        return render(request, 'states/addedge.html', {'edge_exists_error':1,'edge_form':edge_form,'chapter':c,'nodes':chapter_nodes, 'profile':user_obj})



                print(n1,n2)
                Edge.objects.create(first=n1,second=n2,weight=weight, time=time)
           
                edges=Edge.objects.all()
                chapters= Chapter.objects.all()

                context = {'edge_added':1,
                'chapters':chapters,
                'edges':edges, 
                'profile':user_obj}

                return render(request, 'states/edgeadmin.html', context)     
        
        c=Chapter.objects.get(id=chapid)
        chapter_nodes=list()
        chapter_nodes = nodes= Node.objects.filter(state_node__topic__chapter=c).distinct()
        edge_form = forms.edge_form()
        return render(request, 'states/addedge.html', {'edge_form':edge_form,'chapter':c,'nodes':chapter_nodes, 'profile':user_obj})

    else:
        return redirect('/auth/login/')