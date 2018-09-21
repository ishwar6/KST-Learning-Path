# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from chapters.models import Chapter
from django.views.generic import View
from .models import TempActiveNode, UserState
from states.models import Node, State
from django.db.models import Q
from random import choice



class IntroductoryResponse(View):
	the_chapters= Chapter.objects.filter(standard=9)

	def get(self, request):

		student_state_ = UserState.objects.filter(user = self.request.user)
		if student_state_.exists():
			student_state = student_state_.first()
			if student_state.active_part != 0:
				return redirect('assess:active')
		return render(request, 'userstates/initialresponse_form.html', {'chapters': self.the_chapters})
	
	def post(self, request):
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
		for the_chapter in self.the_chapters :
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
						list_of_nodes.append(n)
						the_node= choice(list_of_nodes)
			
			
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


