from django import forms
from . import models


class chapter_form(forms.ModelForm):
	class Meta:
		model = models.Chapter
		fields = ['title', 'gaurd', 'standard', 'image']


class topic_form(forms.ModelForm):
	class Meta:
		model = models.Topic
		fields = ['title', 'content1','content2', 'image1', 'total_test_time_in_minutes','image2']



