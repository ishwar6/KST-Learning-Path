from django.db import models
from django.db.models.signals import pre_save,post_save
from chapters.models import Topic, Chapter
import string
import random


# score_of_i tells the score of illustrations needed to complete illustrations for a particular state

class State(models.Model):
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, blank = True, null = True )
    title = models.TextField(max_length = 120, blank = False, null = False) 
    rate  = models.IntegerField(default=2, help_text='Difficulty of the state')
    time  = models.IntegerField(default=5, help_text='approx time needed to solve this state fully')
    tag   = models.CharField( max_length = 40, blank = True, null = True  )



    def __str__(self):
        return str(self.tag)

    def score_of_i(self):
        rate = self.rate
        if rate == 1:
            return 2
        if rate == 2:
            return 2
        if rate == 3:
            return 4
        if rate == 4:
            return 5
        else:
            return 7

    def score_of_q(self):
        rate = self.rate
        if rate == 1:
            return 3
        if rate == 2:
            return 6
        if rate == 3:
            return 9
        if rate == 4:
            return 11
        else:
            return 14





def state_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        if not instance.tag:
            print('State is sifne')
            chapter = Topic.objects.filter(title = instance.topic).first().chapter
            count   = State.objects.filter(topic__chapter = chapter).count()
            instance.tag = str(count) + ' - ' + str(chapter)
            instance.save()
post_save.connect(state_created_receiver, sender = State)



class Node(models.Model):
    state_node  = models.ManyToManyField(State)
    credit      = models.IntegerField(default = 0)

    def __str__(self):
        return str(",".join(p.tag for p in self.state_node.all()))

