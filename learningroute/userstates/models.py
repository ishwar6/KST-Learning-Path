from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User = get_user_model()
from chapters.models import Chapter
from states.models import Node

CHAPTER_PROFIENCY= (
    ('beginer','Beginer'),
    ('intermediate','Intermediate'),
    ('advanced','Advanced'),
    ('dont know','Dont Know'),
)


class TempActiveNode(models.Model):
    user                = models.ForeignKey(User, on_delete=  models.CASCADE, blank = True, null = True)
    chapter             = models.ForeignKey(Chapter , on_delete = models.CASCADE,  blank = True, null = True)
    node                = models.ForeignKey(Node , on_delete = models.CASCADE,  blank = True, null = True)
    dont_know_switch    = models.BooleanField(default = 0)
   

    def __str__(self):
        return str(self.user) + ' for the node >> '+ str(self.node)  +' << for the chapter ' + str(self.chapter)

class PracticeChapter(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    chapter         = models.ForeignKey(Chapter, on_delete = models.CASCADE,  blank = True, null = True)
    timedate        = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    def __str__(self):
        return str(self.user) + ' - ' +str(self.chapter)



class UserState(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True)
    active_part        = models.IntegerField(default=0, help_text='It is 0 for entering detail stage, 1 for assessment, 2 for report and 3 to begin learning and ending of assessment' )
    

    def __str__(self):
        return str(self.user) + str(self.active_part)



def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserState.objects.get_or_create(user = instance)
post_save.connect(user_created_receiver, sender = User)

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
