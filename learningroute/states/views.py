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
        pr = User.objects.get(username=request.user)
        chapters=Chapter.objects.all() 
        topics=Topic.objects.all()
        states=State.objects.all()
        #print(pr.first_name)
        

        if request.POST.get('add',False):
            return render(request, 'states/selectchapter.html', {'chapters':chapters, 'profile':pr})


        return render(request, 'states/stateadmin.html', {'topics':topics, 'chapters':chapters, 'states':states, 'profile':pr})
    else:
        return HttpResponse('Some Probem occured')



def stateedit(request, title, topic):

    if request.user.is_authenticated:
        pr = User.objects.get(username=request.user)
        
        if request.POST.get('delete',False):
                t=Topic.objects.get(title=topic)
                s=State.objects.get(title=title, topic=t)
                s.delete()
                return HttpResponse('Deleted State Successfully!')

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

            
            #print(pr.first_name)
        
            topics=Topic.objects.all()
            t=Topic.objects.get(title=topic)
            state=State.objects.get(title=title, topic=t)
            

            return render(request, 'states/stateedit.html', {'topics':topics, 'state':state, 'profile':pr})
    else:
        return HttpResponse('Some Probem occured')


def selectchapter(request,title):
     if request.user.is_authenticated:
        pr = User.objects.get(username=request.user)
        chapter=Chapter.objects.get(title=title)
        topics=Topic.objects.filter(chapter=chapter)
        print(topics)
        return render(request, 'states/selecttopic.html', {'topics':topics, 'profile':pr})


def selecttopic(request,title):
     if request.user.is_authenticated:
        topic=Topic.objects.get(title=title)

        if request.POST.get('add',False):
            pr = User.objects.get(username=request.user)
            title=request.POST.get('title')
            rate=request.POST.get('rate')
            time=request.POST.get('time')
            tag=request.POST.get('tag')
            State.objects.create(topic=topic, title=title,rate=rate,time=time,tag=tag)
            return HttpResponse('State added!')

        pr = User.objects.get(username=request.user)
        
        
        return render(request, 'states/addstate.html', {'topics':topic, 'profile':pr})


def nodeadmin(request):
        if request.user.is_authenticated:
            pr = User.objects.get(username=request.user)
            nodes=Node.objects.all()
            chapters= Chapter.objects.all()

            return render(request, 'states/nodeadmin.html', {'chapters':chapters,'nodes':nodes, 'profile':pr})

def nodeedit(request, nodeid):
    if request.user.is_authenticated:
        pr = User.objects.get(username=request.user)
        node=Node.objects.get(id=nodeid)

        if request.POST.get('delete',False):
            node.delete()
            return HttpResponse('Node deleted Successfully!')


        if request.POST.get('update',False):
            node.description=request.POST.get('description')
            node.credit=request.POST.get('credit')
            node.save()
            return redirect('/states/admin/node/'+str(node.id)+'/')
   

        return render(request, 'states/nodeedit.html', {'node':node, 'profile':pr})




        


def addnode(request,chapid):
    if request.user.is_authenticated:
        if request.POST.get('addnode',False):

            description=request.POST.get('description',False)
            credit=request.POST.get('credit',False)
            addstates=list()
            states=State.objects.all()
            # print(request.POST.get('9',False))
            for i in states:
                print(request.POST.get(str(i.id)))
                if request.POST.get(str(i.id)):
                    addstates.append(i)
            newnode= Node()
            newnode.description=description
            newnode.credit=credit
            newnode.save()

            for i in addstates:
                newnode.state_node.add(i)

            print(newnode)
                    
            return HttpResponse('Nofully!')      

        states=list()
        pr = User.objects.get(username=request.user)
        c=Chapter.objects.get(id=chapid)
        topics=Topic.objects.filter(chapter=c)
        for i in topics:
            if i.chapter == c:
                s=State.objects.filter(topic=i)
                for j in s:
                    states.append(j)
                
        print(states)
        return render(request, 'states/addnode.html', {'chapter':c,'states':states, 'profile':pr})


 
def edgeadmin(request):
    if request.user.is_authenticated:
            pr = User.objects.get(username=request.user)
            edges=Edge.objects.all()
            chapters= Chapter.objects.all()



            return render(request, 'states/edgeadmin.html', {'chapters':chapters,'edges':edges, 'profile':pr})


def edgeedit(request, edgeid):
    if request.user.is_authenticated:
        pr = User.objects.get(username=request.user)
        edge=Edge.objects.get(id=edgeid)

        if request.POST.get('delete',False):
            edge.delete()
            return HttpResponse('Edge deleted Successfully!')


        if request.POST.get('update',False):
            edge.weight=request.POST.get('weight')
            edge.time=request.POST.get('time')
            edge.save()
            return redirect('/states/admin/edge/'+str(edge.id)+'/')
   

        return render(request, 'states/edgeedit.html', {'edge':edge, 'profile':pr})






def addedge(request,chapid):
    if request.user.is_authenticated:
        if request.POST.get('addedge',False):

            weight=request.POST.get('weight',False)
            time=request.POST.get('time',False)

            addnodes=list()
            nodes=Node.objects.all()
            # print(request.POST.get('9',False))
            for i in nodes:
                #print(request.POST.get(str(i.id)))
                if request.POST.get(str(i.id)):
                    addnodes.append(i)

            n1=addnodes[0]
            n2=addnodes[1]

            print(n1,n2)
            Edge.objects.create(first=n1,second=n2,weight=weight, time=time)


            

            
                    
            return HttpResponse('Edge created!')


            
        pr = User.objects.get(username=request.user)
        c=Chapter.objects.get(id=chapid)
        topics=Topic.objects.filter(chapter=c)

        nodes=Node.objects.all()
        states=list()
        chapter_nodes=list()

        for i in nodes:
            print(i.state_node.all())

        for i in topics:
            if i.chapter == c:
                s=State.objects.filter(topic=i)
                for j in s:
                    states.append(j)

        for i in nodes:
            for j in i.state_node.all():
                if  j in states:
                    chapter_nodes.append(i)
                    break
            # if  (i.state_node.all() in states):
            #     print(i)
                
        print(nodes)
        return render(request, 'states/addedge.html', {'chapter':c,'nodes':chapter_nodes, 'profile':pr})