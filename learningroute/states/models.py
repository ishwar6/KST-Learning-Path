from django.db import models
from django.db.models.signals import pre_save,post_save
import string
import random





class State(models.Model):
    title = models.CharField(max_length = 120, blank = False, null = False)
    topic = models.CharField(max_length = 222)
    rate = models.IntegerField()
    time = models.IntegerField()
    tag  = models.CharField( max_length = 15, blank = True, null = True  )


    def __str__(self):
        return self.title + ' - for the topic - ' + self.topic





def id_generator(state_number, size=6, chars=string.ascii_uppercase + string.digits):
    state_number = str(state_number)
    return state_number + '-' + ''.join(random.choice(chars) for _ in range(size))

def rl_pre_save_receiver(sender,instance, *args, **kwargs):
        state_number = int(State.objects.filter(topic__iexact = instance.topic).count()) + 1
        if not instance.tag:
            instance.tag = id_generator(state_number)

pre_save.connect(rl_pre_save_receiver, sender= State)
