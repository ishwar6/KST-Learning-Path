from django.shortcuts import render, redirect
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import utility_kst

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
            state.title=request.POST.get('title')
            state.rate=request.POST.get('rate')
            state.time=request.POST.get('time')
            state.tag=request.POST.get('tag')
            state.save()
            return redirect('/states/admin/'+str(state.title)+'/'+str(state.topic)+'/')

        else:       
            topics=Topic.objects.all()
            t=Topic.objects.get(title=topic)
            state=State.objects.get(title=title, topic=t)
            
            return render(request, 'states/stateedit.html', {'topics':topics, 'state':state, 'profile':user_obj})
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
            title=request.POST.get('title')
            rate=request.POST.get('rate')
            time=request.POST.get('time')
            tag=request.POST.get('tag')
            State.objects.create(topic=topic, title=title,rate=rate,time=time,tag=tag)
            chapters=Chapter.objects.all() 
            topics=Topic.objects.all()
            states=State.objects.all()

            context = {'state_added':1,
            'topics':topics, 
            'chapters':chapters, 
            'states':states, 
            'profile':user_obj}

            return render(request, 'states/stateadmin.html', context)              
              
        return render(request, 'states/addstate.html', {'topics':topic, 'profile':user_obj})
     else:
        return redirect('/auth/login/')


def nodeadmin(request):
        if request.user.is_authenticated:
            user_obj = User.objects.get(username=request.user)
            nodes=Node.objects.all()
            chapters= Chapter.objects.all()

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
            node.description=request.POST.get('description')
            node.credit=request.POST.get('credit')
            node.save()
            return redirect('/states/admin/node/'+str(node.id)+'/')

        return render(request, 'states/nodeedit.html', {'node':node, 'profile':user_obj})
    else:
        return redirect('/auth/login/')



def addnode(request,chapid):
    if request.user.is_authenticated:
        if request.POST.get('addnode',False):
            user_obj = User.objects.get(username=request.user)

            description=request.POST.get('description',False)
            credit=request.POST.get('credit',False)
            selected_states=list()
            states=State.objects.all()
        
            for i in states:
                if request.POST.get(str(i.id)):
                    selected_states.append(i)
            newnode= Node()
            newnode.description=description
            newnode.credit=credit
            newnode.save()

            for i in selected_states:
                newnode.state_node.add(i)

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
        return render(request, 'states/addnode.html', {'chapter':c,'states':states, 'profile':user_obj})
    else:
        return redirect('/auth/login/')


 
def edgeadmin(request):
    if request.user.is_authenticated:
            user_obj = User.objects.get(username=request.user)
            edges=Edge.objects.all()
            chapters= Chapter.objects.all()
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
            edge.weight=request.POST.get('weight')
            edge.time=request.POST.get('time')
            edge.save()
            return redirect('/states/admin/edge/'+str(edge.id)+'/')
   
        return render(request, 'states/edgeedit.html', {'edge':edge, 'profile':user_obj})
    else:
        return redirect('/auth/login/')



def addedge(request,chapid):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
        if request.POST.get('addedge',False):

            weight=request.POST.get('weight',False)
            time=request.POST.get('time',False)

            addnodes=list()
            nodes=Node.objects.all()
            for i in nodes:
                if request.POST.get(str(i.id)):
                    addnodes.append(i)

            n1=addnodes[0]
            n2=addnodes[1]

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
        chapter_nodes = nodes= Node.objects.filter(state_node__topic__chapter=c)

        return render(request, 'states/addedge.html', {'chapter':c,'nodes':chapter_nodes, 'profile':user_obj})

    else:
        return redirect('/auth/login/')