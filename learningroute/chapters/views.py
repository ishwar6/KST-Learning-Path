from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
from chapters.models import Chapter
from .models import Topic

def mainpage(request):
	if request.user.is_authenticated:
		if request.POST.get('add',False):
			title=request.POST.get('title',False)
			gaurd=request.POST.get('gaurd',False)
			standard=request.POST.get('standard',False)
			image=request.FILES.get('photo',None)
			Chapter.objects.create(title=title, gaurd=gaurd, standard=standard, image=image) 
			return HttpResponse('Chapter added!')


		pr = User.objects.get(username=request.user)
		chapters=Chapter.objects.all() 
		return render(request, 'chapters/mainpage.html', {'chapters':chapters, 'profile':pr})


def editchapter(request,chapternumber):
	if request.user.is_authenticated:




		pr = User.objects.get(username=request.user)
		
		if request.POST.get('addtopic',False):
			c=Chapter.objects.get(id=chapternumber)
			title=request.POST.get('title',False)
			content1=request.POST.get('content1',False)
			content2=request.POST.get('content2',False)
			total_test_time_in_minutes=request.POST.get('total_test_time_in_minutes',False)
			image1=request.FILES.get('image1',None)
			image2=request.FILES.get('image2',None)
			Topic.objects.create(chapter=c, title=title, content1=content1,content2=content2, total_test_time_in_minutes=total_test_time_in_minutes, image1=image1 , image2=image2) 
			return HttpResponse('Topic added!')



		if request.POST.get('topicedit',False):
			topicnumber=request.POST.get('topicnumber',False)
			return redirect('/chapters/topic/'+str(topicnumber)+'/')
		c=Chapter.objects.get(id=chapternumber)
		topics=Topic.objects.filter(chapter=c)
		
		if request.POST.get('update',False):
			if request.FILES.get('photo',False) and (not request.POST.get('nophoto',False)):
				c.image = request.FILES.get('photo',False)
			elif request.POST.get('nophoto',False):
				c.image=None
			c.title=request.POST.get('title',False)
			c.gaurd=request.POST.get('gaurd',False)
			c.standard=request.POST.get('standard',False)
			c.save()
			print(c)
			return redirect('/chapters/'+str(c.id)+'/')
		
		print(c)
		return render(request, 'chapters/editchapter.html', {'chapter':c, 'profile':pr, 'topics':topics})




def edittopic(request,topicnumber):
	if request.user.is_authenticated:
		pr = User.objects.get(username=request.user)
		t=Topic.objects.get(id=topicnumber)
		if request.POST.get('delete',False):
			t.delete()
			return HttpResponse('Topic deleted!')



		if request.POST.get('update',False):
			t.title=request.POST.get('title',False)
			t.content1=request.POST.get('content1',False)
			t.content2=request.POST.get('content2',False)
			t.total_test_time_in_minutes=request.POST.get('total_test_time_in_minutes',False)

			if request.FILES.get('image1',False) and (not request.POST.get('nophoto',False)):
				t.image1 = request.FILES.get('image1',False)
			elif request.POST.get('nophoto',False):
				t.image1=None

			if request.FILES.get('image2',False) and (not request.POST.get('noansphoto',False)):
				t.image2 = request.FILES.get('image2',False)
			elif request.POST.get('noansphoto',False):
				t.image2=None

			
			t.save()
			return redirect('/chapters/topic/'+str(t.id)+'/')



		
		
		return render(request, 'chapters/edittopic.html', {'profile':pr, 'topic':t})


	
