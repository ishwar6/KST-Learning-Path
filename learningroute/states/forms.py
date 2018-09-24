from django import forms
from . import models


class state_form(forms.ModelForm):
	class Meta:
		model = models.State
		fields = ['title', 'rate', 'time', 'tag']



