from django.db import models
from states.models import state



class Question(models.Model):
	state          =   models.ForeignKey(Test_topic, on_delete=models.CASCADE)
	text  =   models.CharField(max_length=6600)

	question_image =   models.ImageField(blank=True, null=True, upload_to="questions")
	option1        =   models.CharField(blank=True, max_length=2200)
	option2        =   models.CharField(blank=True, max_length=2200)
	option3        =   models.CharField(blank=True, max_length=2200)
	option4        =   models.CharField(blank=True, max_length=2200)
	op1            =   models.BooleanField(default=False)
	op2            =   models.BooleanField(default=False)
	op3            =   models.BooleanField(default=False)
	op4            =   models.BooleanField(default=False)
	time           =   models.IntegerField(default=0)
	score          =   models.IntegerField(default=0)
	integer_type   =   models.BooleanField(default=False)
	single_option  =   models.BooleanField(default=False)
	integeral_answer = models.CharField(blank=True, max_length=200)
	answer_image   =   models.ImageField(blank=True, null=True, upload_to="answers")
	answer_text    =   models.CharField(blank=True, max_length=200)


	def __str__(self):
		return self.text
