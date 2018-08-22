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


    def __str__(self):
        return str(self.user) + ' - ' +str(self.state)







CHAPTER_PROFIENCY= (
    ('beginer','Beginer'),
    ('intermediate','Intermediate'),
    ('advanced','Advanced')
)
class Proficiency(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    chapter= models.ForeignKey('chapters.Chapter', on_delete=models.CASCADE)
    level= models.CharField(max_length = 60, choices = CHAPTER_PROFIENCY, blank=False)
    significance= models.IntegerField()

    def __str__(self):
        return str(self.user) + ' have ' + str(self.level) + ' level for the chapter:- ' + str(self.chapter)







class TempActiveNode(models.Model):
    user = models.ForeignKey(User, on_delete=  models.CASCADE)
    chapter = models.ForeignKey('chapters.Chapter', on_delete = models.CASCADE)
    node = models.ForeignKey('states.Node', on_delete = models.CASCADE, default = None)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.node) + ' - for the chapter ' + str(self.chapter)














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
