from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
from chapters.models import Chapter
from .models import Topic
from .import forms

def mainpage(request):
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		chapters=Chapter.objects.all() 

		if request.POST.get('add',False):
			chapter_form = forms.chapter_form(request.POST, request.FILES)
			if chapter_form.is_valid():
				chapter_form.save()
				chapter_form = forms.chapter_form()
				return render(request, 'chapters/mainpage.html', {'chapter_form':chapter_form,'chapter_added':1,'chapters':chapters, 'profile':user_obj})
			else:
				chapter_form = forms.chapter_form()
				return render(request, 'chapters/mainpage.html', {'chapter_form':chapter_form,'chapter_added_error':1,'chapters':chapters, 'profile':user_obj})

		chapter_form = forms.chapter_form()
		return render(request, 'chapters/mainpage.html', {'chapter_form':chapter_form,'chapters':chapters, 'profile':user_obj})


def editchapter(request,chapternumber):
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		current_chapter=Chapter.objects.get(id=chapternumber)
		topics=Topic.objects.filter(chapter=current_chapter)
		chapter_form = forms.chapter_form(instance=current_chapter)
		print(chapter_form)

		if request.POST.get('delete',False):
			chapters=Chapter.objects.all() 
			current_chapter.delete()
			return render(request, 'chapters/mainpage.html', {'chapter_form':chapter_form,'chapter_deleted':1,'chapters':chapters, 'profile':user_obj})
		
		if request.POST.get('addtopic',False):
			current_chapter=Chapter.objects.get(id=chapternumber)
			topic_form = forms.topic_form(request.POST, request.FILES)
			if topic_form.is_valid():
				new_topic = topic_form.save(commit= False)
				new_topic.chapter = current_chapter
				new_topic.save()
				topic_form = forms.topic_form()

				context = {'topic_added':1,
				'topic_form':topic_form,
				'chapter_form':chapter_form,
				'chapter':current_chapter, 
				'profile':user_obj, 
				'topics':topics}

				return render(request, 'chapters/editchapter.html', context)
			else:
				context = {'topic_added_error':1,
				'topic_form':topic_form,
				'chapter_form':chapter_form,
				'chapter':current_chapter, 
				'profile':user_obj, 
				'topics':topics
				}
				return render(request, 'chapters/editchapter.html', context)



		if request.POST.get('topicedit',False):
			topicnumber=request.POST.get('topicnumber',False)
			return redirect('/chapters/topic/'+str(topicnumber)+'/')
		
		if request.POST.get('update',False):
			chapter_form = forms.chapter_form(request.POST, request.FILES, instance=current_chapter)
			if chapter_form.is_valid():
				chapter_form.save()
				topic_form = forms.topic_form()
				return render(request, 'chapters/editchapter.html', {'topic_form':topic_form,'chapter':current_chapter,'chapter_form':chapter_form, 'profile':user_obj, 'topics':topics})
			
			else:
				chapter_form = forms.chapter_form(instance=current_chapter)
				topic_form = forms.topic_form()
				return render(request, 'chapters/editchapter.html', {'chapter_update_error':1,'topic_form':topic_form,'chapter':current_chapter,'chapter_form':chapter_form, 'profile':user_obj, 'topics':topics})


			
		topic_form = forms.topic_form()
		return render(request, 'chapters/editchapter.html', {'chapter_form':chapter_form,'topic_form':topic_form, 'chapter':current_chapter,'profile':user_obj, 'topics':topics})




def edittopic(request,topicnumber):
	if request.user.is_authenticated:
		user_obj = User.objects.get(username=request.user)
		current_topic=Topic.objects.get(id=topicnumber)
		chapter=current_topic.chapter
		topics=Topic.objects.filter(chapter=chapter)
		chapter_form = forms.chapter_form()

		if request.POST.get('delete',False):
			current_topic.delete()
			topic_form = forms.topic_form()
			chapter_form=forms.chapter_form(instance=chapter)

			context = {'topic_deleted':1,
			'topic_form':topic_form,
			'chapter':chapter, 
			'profile':user_obj, 
			'chapter_form':chapter_form,
			'topics':topics}

			return render(request, 'chapters/editchapter.html', context)

		if request.POST.get('update',False):
			topic_form = forms.topic_form(request.POST, request.FILES, instance=current_topic)
			if topic_form.is_valid():
				new_topic = topic_form.save(commit= False)
				new_topic.chapter = chapter
				new_topic.save()
				topic_form = forms.topic_form(instance=new_topic)		
				return render(request, 'chapters/edittopic.html', {'topic_form':topic_form,'profile':user_obj, 'topic':current_topic})

			else:
				topic_form = forms.topic_form(instance=current_topic)
				return render(request, 'chapters/edittopic.html', {'topic_update_error':1,'topic_form':topic_form,'profile':user_obj, 'topic':current_topic})

		topic_form = forms.topic_form(instance=current_topic)
		return render(request, 'chapters/edittopic.html', {'topic_form':topic_form,'profile':user_obj, 'topic':current_topic})


	
