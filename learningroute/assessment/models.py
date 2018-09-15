from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from chapters.models import Chapter
from states.models import State
from userstates.models import UserCurrentNode 
# Create your models here.


class TestsTaken(models.Model):
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	chapter= models.ForeignKey(Chapter, on_delete=models.CASCADE)
	resultant_node= models.ForeignKey(UserCurrentNode, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return str(self.user)+str(self.chapter)



class User_submission(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	state=models.ForeignKey(State, on_delete=models.	CASCADE)
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
