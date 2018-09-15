from django.db import models
from states.models import State
from django.db.models.signals import pre_save,post_save
from django.contrib.auth import get_user_model
User = get_user_model()
import random
import os

def upload_image_path_questions(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "questions/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class Question(models.Model):
	DIFFICULTY = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
       
    )
	state         	 =   models.ForeignKey(State, on_delete=models.CASCADE)
	text  			 =   models.TextField()
	question_image	 =   models.FileField(upload_to = upload_image_path_questions, null = True, blank = True)
	difficulty       =   models.CharField(max_length = 10, choices = DIFFICULTY, default = 1)

	option1          =   models.CharField(blank=True, max_length=2200)
	option2          =   models.CharField(blank=True, max_length=2200)
	option3          =   models.CharField(blank=True, max_length=2200)
	option4          =   models.CharField(blank=True, max_length=2200)

	op1              =   models.BooleanField(default=False)
	op2              =   models.BooleanField(default=False)
	op3              =   models.BooleanField(default=False)
	op4              =   models.BooleanField(default=False)

	time             =   models.IntegerField(default=0)
	score            =   models.IntegerField(default=0)
	integer_type     =   models.BooleanField(default=False)
	single_option    =   models.BooleanField(default=False)
	integeral_answer = models.CharField(blank=True, max_length=100)
	answer_image     =   models.FileField(upload_to = upload_image_path_questions, null = True, blank = True)
	answer_text      =   models.TextField()
	counts    	     =   models.IntegerField(blank = True, null = True, help_text='Leave it blank')


	def __str__(self):
		return self.text







def ques_created_reciever(sender, instance, *args, **kwargs):
	illust_last     =  Question.objects.filter(state = instance.state)
	if not illust_last.exists():
		instance.counts = 1
	else:
		last  =  illust_last.last().counts
		if not instance.counts:
			instance.counts = last + 1


        
pre_save.connect(ques_created_reciever, sender=Question)





class QuestionResponse(models.Model):
	user					=   models.ForeignKey(User, on_delete=models.CASCADE)
	question			    =   models.ForeignKey(Question, on_delete=models.CASCADE)
	op1						=   models.BooleanField(default=False)
	op2						=   models.BooleanField(default=False)
	op3						=   models.BooleanField(default=False)
	op4						=   models.BooleanField(default=False)
	integer_type_submission =   models.CharField(blank=True, max_length=200)
	correct				    =   models.BooleanField(default=False)


	def __str__(self):
		return str(self.question.id) +'  ' +  str(self.user) +'  ' + str(self.correct)
