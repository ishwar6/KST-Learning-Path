from django import forms
from . import models


class state_form(forms.ModelForm):
	class Meta:
		model = models.State
		fields = ['title', 'rate', 'time', 'tag']



class node_form(forms.ModelForm):
	class Meta:
		model = models.Node
		fields = ['description', 'credit']


class edge_form(forms.ModelForm):
	class Meta:
		model = models.Edge
		fields = ['weight', 'time']	