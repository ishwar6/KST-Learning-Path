from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User = get_user_model()

class UserCurrentState(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    state       = models.ForeignKey('states.State', on_delete= models.CASCADE, default = None)
    stage       = models.IntegerField(default = 0)
    total_time  = models.IntegerField(blank = True, null = True)
    timedate    = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return str(self.user) + ' - ' + str(self.stage)



def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        CurrentUserState.objects.get_or_create(user = instance)
post_save.connect(user_created_receiver, sender = User)


class UserCompletedState(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    state       = models.ForeignKey('states.State', on_delete= models.CASCADE, default = None)
    correct     = models.IntegerField(default = 0)
    incorrect   = models.IntegerField(default = 0)
    time_taken  = models.IntegerField(blank = True, null = True)
    start_time  = models.IntegerField(blank = True, null = True)
    timedate    = models.DateTimeField(auto_now_add = True, blank = True, null = True)

'''
are you surely in claass 9 
'''
CHAPTER_PROFIENCY= (
    ('beginer','Beginer'),
    ('intermediate','Intermediate'),
    ('expert','Expert')
)
class Initialresponse(models.Model):
    polynomial_proficieny= models.CharField(max_length = 60, default = 'intermediate', choices = CHAPTER_PROFIENCY)
    lineq_two_variable_proficiency_prof= models.CharField(max_length = 60, default = 'intermediate', choices = CHAPTER_PROFIENCY)
    triangels_proficiency= models.CharField(max_length = 60, default = 'intermediate', choices = CHAPTER_PROFIENCY)
    quadrilateral_proficiency= models.CharField(max_length = 60, default = 'intermediate', choices = CHAPTER_PROFIENCY)
    time_willing_to_work=models.IntegerField()

'''
Functions to be created:

1. Active learning route of the student
2. Active state of the student
3. how to switch the learning route on the basis of response of questions
4. How many time a student logged in today, in a week and month data
5. To display stage (content, illus, question of given state) when student loggs back
in where he left
6. To display ready to learn topic to the student
7. To display list of all mastered topic to the student
8. Estimated time left to clear a chapter for a student
9. To make a don't know button for each question if student have no idea of it at All
10. Feedback from the student to make more explanation next time
'''