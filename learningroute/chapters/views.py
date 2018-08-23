from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
from chapters.models import Chapter
from .models import Topic

def mainpage(request):
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		chapters=Chapter.objects.all() 

		if request.POST.get('add',False):
			title=request.POST.get('title',False)
			gaurd=request.POST.get('gaurd',False)
			standard=request.POST.get('standard',False)
			image=request.FILES.get('photo',None)
			Chapter.objects.create(title=title, gaurd=gaurd, standard=standard, image=image) 
			return render(request, 'chapters/mainpage.html', {'chapter_added':1,'chapters':chapters, 'profile':user_obj})
		
		return render(request, 'chapters/mainpage.html', {'chapters':chapters, 'profile':user_obj})


def editchapter(request,chapternumber):
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		current_chapter=Chapter.objects.get(id=chapternumber)
		topics=Topic.objects.filter(chapter=current_chapter)

		if request.POST.get('delete',False):
			chapters=Chapter.objects.all() 
			current_chapter.delete()
			return render(request, 'chapters/mainpage.html', {'chapter_deleted':1,'chapters':chapters, 'profile':user_obj})
		
		if request.POST.get('addtopic',False):
			current_chapter=Chapter.objects.get(id=chapternumber)
			title=request.POST.get('title',False)
			content1=request.POST.get('content1',False)
			content2=request.POST.get('content2',False)
			total_test_time_in_minutes=request.POST.get('total_test_time_in_minutes',False)
			image1=request.FILES.get('image1',None)
			image2=request.FILES.get('image2',None)
			Topic.objects.create(chapter=current_chapter,
			 					 title=title,
			  					 content1=content1,
			  					 content2=content2, 
			  					 total_test_time_in_minutes=total_test_time_in_minutes, 
			  					 image1=image1 , 
			  					 image2=image2) 

			context = {'topic_added':1,
			'chapter':current_chapter, 
			'profile':user_obj, 
			'topics':topics}

			return render(request, 'chapters/editchapter.html', context)

		if request.POST.get('topicedit',False):
			topicnumber=request.POST.get('topicnumber',False)
			return redirect('/chapters/topic/'+str(topicnumber)+'/')
		
		if request.POST.get('update',False):
			if request.FILES.get('photo',False) and (not request.POST.get('nophoto',False)):
				current_chapter.image = request.FILES.get('photo',False)
			elif request.POST.get('nophoto',False):
				current_chapter.image=None
			current_chapter.title=request.POST.get('title',False)
			current_chapter.gaurd=request.POST.get('gaurd',False)
			current_chapter.standard=request.POST.get('standard',False)
			current_chapter.save()
			return redirect('/chapters/'+str(current_chapter.id)+'/')
		
		return render(request, 'chapters/editchapter.html', {'chapter':current_chapter, 'profile':user_obj, 'topics':topics})




def edittopic(request,topicnumber):
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		current_topic=Topic.objects.get(id=topicnumber)
		chapter=current_topic.chapter
		topics=Topic.objects.filter(chapter=chapter)

		if request.POST.get('delete',False):
			current_topic.delete()

			context = {'topic_deleted':1,
			'chapter':chapter, 
			'profile':user_obj, 
			'topics':topics}

			return render(request, 'chapters/editchapter.html', context)

		if request.POST.get('update',False):
			current_topic.title=request.POST.get('title',False)
			current_topic.content1=request.POST.get('content1',False)
			current_topic.content2=request.POST.get('content2',False)
			current_topic.total_test_time_in_minutes=request.POST.get('total_test_time_in_minutes',False)

			if request.FILES.get('image1',False) and (not request.POST.get('nophoto',False)):
				current_topic.image1 = request.FILES.get('image1',False)
			elif request.POST.get('nophoto',False):
				current_topic.image1=None

			if request.FILES.get('image2',False) and (not request.POST.get('noansphoto',False)):
				current_topic.image2 = request.FILES.get('image2',False)
			elif request.POST.get('noansphoto',False):
				current_topic.image2=None
			
			current_topic.save()
			return redirect('/chapters/topic/'+str(current_topic.id)+'/')
		
		return render(request, 'chapters/edittopic.html', {'profile':user_obj, 'topic':current_topic})


	
