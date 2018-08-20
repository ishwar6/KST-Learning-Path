from django.db import models
from django.contrib.auth.models import User
from chapters.models import Topic, Question

# Create your models here.


class TestsTaken(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
	score=models.IntegerField(default=0)
	def __str__(self):
		return str(self.user)+str(self.topic)



class User_submission(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	op1=models.BooleanField(default=False)
	op2=models.BooleanField(default=False)
	op3=models.BooleanField(default=False)
	op4=models.BooleanField(default=False)
	integer_type_submission=models.CharField(blank=True, max_length=200)
	time_of_sumbission=models.CharField(blank=True, max_length=200)
	submitted_by_user=models.BooleanField(default=False)
	correctans=models.BooleanField(default=False)
	def __str__(self):
		return str(self.question.id)+str(self.user)
